import json
import hashlib
import uuid
import datetime

from typing import List, Dict, Any

from sqlalchemy import select, func, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from fastapi.encoders import jsonable_encoder

from app.core.cache.redis_client import redis_client
from app.shared.filters.filter_builder import FilterBuilder
from app.shared.filters.search_builder import SearchBuilder
from app.shared.filters.sort_builder import SortBuilder
from app.shared.pagination.paginator import Paginator


CACHE_VERSION = "v1"


def to_json(obj):

    if isinstance(obj, uuid.UUID):
        return str(obj)

    if isinstance(obj, datetime.datetime):
        return obj.isoformat()

    if isinstance(obj, datetime.date):
        return obj.isoformat()

    if isinstance(obj, dict):
        return {
            key: to_json(value)
            for key, value in obj.items()
        }

    if isinstance(obj, (list, tuple, set)):
        return [
            to_json(value)
            for value in obj
        ]

    if hasattr(obj, "__table__"):
        return {
            c.name: to_json(
                getattr(obj, c.name)
            )
            for c in obj.__table__.columns
        }

    return obj


def apply_select_fields(
    model,
    fields: list | None
):

    if not fields:
        return None

    cols = []

    for field in fields:

        if hasattr(model, field):

            cols.append(
                getattr(model, field)
            )

    return cols if cols else None


def rows_to_dicts(
    rows,
    columns
):

    return [
        dict(zip(columns, row))
        for row in rows
    ]


class QueryEngine:

    def __init__(
        self,
        session: AsyncSession,
        model,
    ):

        self.session = session
        self.model = model

        self.base_stmt = select(
            model
        )

    # =========================================================
    # MODEL → DICT
    # =========================================================

    def _model_to_dict(
        self,
        obj,
    ) -> dict:

        if not hasattr(
            obj,
            "__table__"
        ):
            return obj

        return {
            column.name: getattr(
                obj,
                column.name
            )
            for column in obj.__table__.columns
        }

    def _row_to_dict(
        self,
        row,
    ) -> dict:

        return dict(
            row._mapping
        )

    # =========================================================
    # CACHE KEY
    # =========================================================

    def _build_cache_key(
        self,
        payload: dict
    ):

        raw = json.dumps(
            payload,
            sort_keys=True,
            default=str,
        ).encode()

        digest = hashlib.sha256(
            raw
        ).hexdigest()

        return (
            f"{CACHE_VERSION}:query:"
            f"{self.model.__name__}:"
            f"{digest}"
        )

    def serialize(
        self,
        obj
    ):

        if hasattr(
            obj,
            "__table__"
        ):

            return {
                c.name: getattr(
                    obj,
                    c.name
                )
                for c in obj.__table__.columns
            }

        return obj

    # =========================================================
    # CACHE TTL
    # =========================================================

    def _get_ttl(
        self,
        search: str | None,
        filters: dict | None
    ):

        if search:
            return 60

        if filters:
            return 180

        return 600

    # =========================================================
    # CACHE INVALIDATION
    # =========================================================

    async def _invalidate(self):

        if not redis_client:
            return

        pattern = (
            f"{CACHE_VERSION}:query:"
            f"{self.model.__name__}:*"
        )

        tag = (
            f"{CACHE_VERSION}:query:"
            f"{self.model.__name__}:tags"
        )

        try:

            cached_keys = (
                await redis_client.smembers(
                    tag
                )
            )

            if cached_keys:

                await redis_client.delete(
                    *list(cached_keys),
                    tag
                )

                return

        except Exception:
            pass

        try:

            async for key in redis_client.scan_iter(
                match=pattern
            ):

                await redis_client.delete(
                    key
                )

        except Exception:
            pass

    # =========================================================
    # ALL
    # =========================================================

    async def all(
        self,
        select_fields=None
    ):

        stmt = self.base_stmt

        if select_fields:

            cols = [
                getattr(
                    self.model,
                    field
                )
                for field in select_fields
                if hasattr(
                    self.model,
                    field
                )
            ]

            if cols:

                stmt = select(
                    *cols
                )

        result = await self.session.execute(
            stmt
        )

        rows = result.all()

        if select_fields:

            return rows_to_dicts(
                rows,
                select_fields
            )

        return [
            to_json(item)
            for item in rows
        ]

    # =========================================================
    # FIRST
    # =========================================================

    async def first(
        self,
        filters: dict = None,
        search: str = None,
        search_fields: list = None,
        sort_by: str = None,
        direction: str = "asc",
        select_fields=None
    ):

        stmt = self.base_stmt

        # SELECT
        if select_fields:

            cols = [
                getattr(
                    self.model,
                    field
                )
                for field in select_fields
                if hasattr(
                    self.model,
                    field
                )
            ]

            if cols:

                stmt = select(
                    *cols
                )

        # FILTERS
        if filters:

            stmt = FilterBuilder.apply(
                stmt,
                self.model,
                filters
            )

        # SEARCH
        if search:

            stmt = SearchBuilder.apply(
                stmt,
                self.model,
                search,
                search_fields or []
            )

        # SORT
        if sort_by:

            stmt = SortBuilder.apply(
                stmt,
                self.model,
                sort_by,
                direction
            )

        stmt = stmt.limit(1)

        result = await self.session.execute(
            stmt
        )

        row = result.first()

        if not row:
            return None

        if select_fields:

            return dict(
                zip(
                    select_fields,
                    row
                )
            )

        return row[0]

    # =========================================================
    # FIND
    # =========================================================

    async def find(
        self,
        filters: dict = None,
        search: str = None,
        search_fields: list = None,
        sort_by: str = None,
        direction: str = "asc",
        select_fields=None
    ):

        stmt = self.base_stmt

        # SELECT
        if select_fields:

            cols = [
                getattr(
                    self.model,
                    field
                )
                for field in select_fields
                if hasattr(
                    self.model,
                    field
                )
            ]

            if cols:

                stmt = select(
                    *cols
                )

        # FILTERS
        if filters:

            stmt = FilterBuilder.apply(
                stmt,
                self.model,
                filters
            )

        # SEARCH
        if search:

            stmt = SearchBuilder.apply(
                stmt,
                self.model,
                search,
                search_fields or []
            )

        # SORT
        if sort_by:

            stmt = SortBuilder.apply(
                stmt,
                self.model,
                sort_by,
                direction
            )

        result = await self.session.execute(
            stmt
        )

        rows = result.all()

        if select_fields:

            return rows_to_dicts(
                rows,
                select_fields
            )

        return [
            to_json(item)
            for item in rows
        ]

    # =========================================================
    # LIST
    # =========================================================

    async def list_(
        self,
        filters=None,
        search=None,
        search_fields=None,
        sort_by=None,
        direction="asc",
        page=1,
        per_page=20,
        select_fields=None
    ):

        use_projection = bool(
            select_fields
        )

        cache_payload = {
            "model": self.model.__name__,
            "filters": filters or {},
            "search": search,
            "search_fields": search_fields or [],
            "sort": sort_by,
            "direction": direction,
            "page": page,
            "per_page": per_page,
            "select_fields": select_fields,
        }

        cache_key = self._build_cache_key(
            cache_payload
        )

        # =====================================================
        # CACHE HIT
        # =====================================================

        if redis_client:

            cached = await redis_client.get(
                cache_key
            )

            if cached:

                return json.loads(
                    cached
                )

        # =====================================================
        # QUERY
        # =====================================================

        if use_projection:

            stmt = select(
                *[
                    getattr(
                        self.model,
                        field
                    )
                    for field in select_fields
                    if hasattr(
                        self.model,
                        field
                    )
                ]
            )

        else:

            stmt = select(
                self.model
            )

        # =====================================================
        # FILTERS
        # =====================================================

        if filters:

            stmt = FilterBuilder.apply(
                stmt,
                self.model,
                filters
            )

        # =====================================================
        # SEARCH
        # =====================================================

        if search:

            stmt = SearchBuilder.apply(
                stmt,
                self.model,
                search,
                search_fields or []
            )

        # =====================================================
        # SORT
        # =====================================================

        if sort_by:

            stmt = SortBuilder.apply(
                stmt,
                self.model,
                sort_by,
                direction
            )

        # =====================================================
        # PAGINATION
        # =====================================================

        result = await Paginator.paginate(
            self.session,
            stmt,
            page,
            per_page
        )

        raw_items = result.get(
            "items",
            []
        )

        # =====================================================
        # SERIALIZATION
        # =====================================================

        if use_projection:

            items = [
                dict(
                    row._mapping
                )
                for row in raw_items
            ]

        else:

            items = [
                self._model_to_dict(
                    row
                )
                for row in raw_items
            ]

        items = [
            {
                key: to_json(value)
                for key, value in item.items()
            }
            for item in items
        ]

        response = {
            "items": items,
            "total": result.get(
                "total",
                0
            ),
            "page": page,
            "per_page": per_page,
        }

        # =====================================================
        # CACHE STORE
        # =====================================================

        if redis_client:

            ttl = self._get_ttl(
                search,
                filters
            )

            await redis_client.setex(
                cache_key,
                ttl,
                json.dumps(
                    jsonable_encoder(
                        response
                    )
                )
            )

            tag = (
                f"{CACHE_VERSION}:query:"
                f"{self.model.__name__}:tags"
            )

            await redis_client.sadd(
                tag,
                cache_key
            )

        return response

    # =========================================================
    # COUNT
    # =========================================================

    async def count(
        self,
        filters: dict = None
    ):

        stmt = select(
            func.count()
        ).select_from(
            self.model
        )

        if filters:

            stmt = FilterBuilder.apply(
                stmt,
                self.model,
                filters
            )

        return await self.session.scalar(
            stmt
        )

    # =========================================================
    # CREATE
    # =========================================================

    async def create(
        self,
        **data
    ):

        try:

            obj = self.model(
                **data
            )

            self.session.add(
                obj
            )

            await self.session.commit()

            await self.session.refresh(
                obj
            )

            await self._invalidate()

            return obj

        except SQLAlchemyError:

            await self.session.rollback()
            raise

    # =========================================================
    # FAST CREATE
    # =========================================================

    async def fast_create(
        self,
        **data
    ):

        try:

            stmt = (
                insert(
                    self.model
                )
                .values(**data)
                .returning(
                    self.model
                )
            )

            result = await self.session.execute(
                stmt
            )

            obj = result.scalar_one()

            await self.session.commit()

            await self._invalidate()

            return obj

        except SQLAlchemyError:

            await self.session.rollback()
            raise

    # =========================================================
    # BULK CREATE
    # =========================================================

    async def bulk_create(
        self,
        data: List[Dict[str, Any]]
    ):

        try:

            if not data:
                return []

            stmt = (
                insert(
                    self.model
                )
                .returning(
                    self.model
                )
            )

            result = await self.session.execute(
                stmt,
                data
            )

            objs = result.scalars().all()

            await self.session.commit()

            await self._invalidate()

            return objs

        except SQLAlchemyError:

            await self.session.rollback()
            raise

    # =========================================================
    # GET
    # =========================================================

    async def get(
        self,
        id_,
        select_fields=None
    ):

        stmt = (
            select(
                self.model
            )
            .where(
                self.model.id == id_
            )
        )

        if select_fields:

            cols = [
                getattr(
                    self.model,
                    field
                )
                for field in select_fields
                if hasattr(
                    self.model,
                    field
                )
            ]

            if cols:

                stmt = (
                    select(*cols)
                    .where(
                        self.model.id == id_
                    )
                )

        result = await self.session.execute(
            stmt
        )

        if select_fields:

            row = result.first()

            if not row:
                return None

            return dict(
                zip(
                    select_fields,
                    row
                )
            )

        return result.scalar_one_or_none()

    # =========================================================
    # UPDATE
    # =========================================================

    async def update(
        self,
        id_,
        **data
    ):

        try:

            stmt = (
                select(
                    self.model
                )
                .where(
                    self.model.id == id_
                )
            )

            result = await self.session.execute(
                stmt
            )

            obj = result.scalar_one_or_none()

            if not obj:
                return None

            for key, value in data.items():

                setattr(
                    obj,
                    key,
                    value
                )

            await self.session.commit()

            await self.session.refresh(
                obj
            )

            await self._invalidate()

            return obj

        except SQLAlchemyError:

            await self.session.rollback()
            raise

    # =========================================================
    # UPDATE NO SCOPE
    # =========================================================

    async def update_no_scope(
        self,
        id_,
        **data
    ):

        return await self.update(
            id_,
            **data
        )

    # =========================================================
    # UPDATE MANY
    # =========================================================

    async def update_many(
        self,
        filters: dict,
        **data
    ):

        try:

            stmt = update(
                self.model
            )

            if filters:

                stmt = FilterBuilder.apply(
                    stmt,
                    self.model,
                    filters
                )

            stmt = stmt.values(
                **data
            )

            result = await self.session.execute(
                stmt
            )

            await self.session.commit()

            await self._invalidate()

            return result.rowcount

        except SQLAlchemyError:

            await self.session.rollback()
            raise

    # =========================================================
    # FAST UPDATE
    # =========================================================

    async def fast_update(
        self,
        id_,
        **data
    ):

        try:

            stmt = (
                update(
                    self.model
                )
                .where(
                    self.model.id == id_
                )
                .values(
                    **data
                )
            )

            result = await self.session.execute(
                stmt
            )

            await self.session.commit()

            await self._invalidate()

            return result.rowcount > 0

        except SQLAlchemyError:

            await self.session.rollback()
            raise

    # =========================================================
    # DELETE
    # =========================================================

    async def delete(
        self,
        id_
    ):

        try:

            obj = await self.session.get(
                self.model,
                id_
            )

            if not obj:
                return None

            await self.session.delete(
                obj
            )

            await self.session.commit()

            await self._invalidate()

            return True

        except SQLAlchemyError:

            await self.session.rollback()
            raise