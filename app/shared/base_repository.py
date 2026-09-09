from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.query_engine import QueryEngine

import datetime
import uuid


class BaseRepository:

    model = None

    def __init__(self, db: AsyncSession):

        if self.model is None:
            raise ValueError(
                "Repository must define a model"
            )

        self.db = db

        self.engine = QueryEngine(
            session=db,
            model=self.model,
        )

    # ========================
    # JSON
    # ========================

    def to_json(self, obj):

        if isinstance(obj, uuid.UUID):
            return str(obj)

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        if hasattr(obj, "__table__"):
            return {
                c.name: self.to_json(
                    getattr(obj, c.name)
                )
                for c in obj.__table__.columns
            }

        return obj

    # ========================
    # CORE CRUD
    # ========================

    async def create(self, **data):
        return await self.engine.create(**data)

    async def fast_create(self, **data):
        return await self.engine.fast_create(**data)

    async def bulk_create(self, data):
        return await self.engine.bulk_create(data)

    async def get(self, id_, select_fields=None):
        return await self.engine.get(
            id_,
            select_fields=select_fields
        )

    async def get_presented(
        self,
        id_,
        select_fields=None
    ):
        return await self.engine._present_record(
            await self.engine.get(
                id_,
                select_fields=select_fields
            )
        )

    async def all(self, select_fields=None):
        return await self.engine.all(
            select_fields=select_fields
        )

    async def update(self, id_, **data):
        return await self.engine.update(
            id_,
            **data
        )

    async def update_no_scope(self, id_, **data):
        return await self.engine.update_no_scope(
            id_,
            **data
        )

    async def fast_update(self, id_, **data):
        return await self.engine.fast_update(
            id_,
            **data
        )

    async def update_many(
        self,
        filters: dict,
        **data
    ):
        return await self.engine.update_many(
            filters,
            **data
        )

    async def delete(self, id_):
        return await self.engine.delete(id_)

    async def count(
        self,
        filters: dict = {}
    ):
        return await self.engine.count(filters)

    # ========================
    # LIST
    # ========================

    async def list(
        self,
        filters: dict = None,
        search: str = None,
        search_fields: list = None,
        sort_by: str = None,
        direction: str = "asc",
        page: int = 1,
        per_page: int = 20,
        select_fields=None
    ):

        return await self.engine.list_(
            filters=filters,
            search=search,
            search_fields=search_fields,
            sort_by=sort_by,
            direction=direction,
            page=page,
            per_page=per_page,
            select_fields=select_fields
        )

    async def find(
        self,
        filters: dict = None,
        search: str = None,
        search_fields: list = None,
        sort_by: str = None,
        direction: str = "asc",
        select_fields=None
    ) -> list:

        return await self.engine.find(
            filters=filters,
            search=search,
            search_fields=search_fields,
            sort_by=sort_by,
            direction=direction,
            select_fields=select_fields
        )

    async def first(
        self,
        filters: dict = None,
        search: str = None,
        search_fields: list = None,
        sort_by: str = None,
        direction: str = "asc",
        select_fields=None
    ) -> dict:

        return await self.engine.first(
            filters=filters,
            search=search,
            search_fields=search_fields,
            sort_by=sort_by,
            direction=direction,
            select_fields=select_fields
        )