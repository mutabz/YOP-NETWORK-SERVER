# app/shared/data_pipeline/services/data_pipeline_service.py

from typing import Any
from decimal import Decimal
from sqlalchemy import inspect
from sqlalchemy.orm.attributes import NO_VALUE

from app.core.context.request_context import current_identity
from app.shared.data_pipeline.factories import DataPipelineFactory


class DataPipelineService:

    def __init__(self, session):
        self._pipeline = None
        self._session = session
        self._settings_context = None
        self._company_id = None

    # =========================================================
    # SETUP
    # =========================================================

    async def _ensure_setup(self) -> bool:

        identity = current_identity.get()
        if not identity:
            return False

        if not self._session:
            return False

        company_id = identity.company_id

        if not company_id:
            return False

        if (
            self._pipeline is not None
            and self._settings_context is not None
            and self._company_id == company_id
        ):
            return True

        (
            self._pipeline,
            self._settings_context,
        ) = await DataPipelineFactory.create(
            session=self._session,
            company_id=company_id,
        )

        self._company_id = company_id

        return True

    # =========================================================
    # SQLALCHEMY ORM → DICT
    # =========================================================

    @classmethod
    def _model_to_dict(
        cls,
        obj: Any,
        visited: set[int] | None = None,
    ) -> dict:

        if visited is None:
            visited = set()

        object_id = id(obj)

        # ---------------------------------------------
        # Circular reference protection
        # ---------------------------------------------

        if object_id in visited:
            return {}

        # Add ONLY for the current recursion path
        visited.add(object_id)

        try:
            mapper = inspect(obj).mapper

            result = {}

            # =========================================
            # COLUMNS
            # =========================================

            for column in mapper.column_attrs:

                key = column.key

                result[key] = getattr(obj, key)

            # =========================================
            # RELATIONSHIPS
            # =========================================

            for relationship in mapper.relationships:

                key = relationship.key

                attribute = inspect(obj).attrs[key]

                # -------------------------------------
                # Do not trigger lazy loading
                # -------------------------------------

                if attribute.loaded_value is NO_VALUE:
                    continue

                value = attribute.loaded_value

                # -------------------------------------
                # Collection relationship
                # -------------------------------------

                if relationship.uselist:

                    if value is None:
                        result[key] = []

                    else:
                        result[key] = [
                            cls._normalize(
                                item,
                                visited=visited,
                            )
                            for item in value
                        ]

                # -------------------------------------
                # Single relationship
                # -------------------------------------

                else:

                    if value is None:
                        result[key] = None

                    else:
                        result[key] = cls._normalize(
                            value,
                            visited=visited,
                        )

            return result

        finally:
            # -----------------------------------------
            # IMPORTANT
            #
            # Remove from current recursion path.
            #
            # This allows another object to reference
            # the same SQLAlchemy object later.
            # -----------------------------------------

            visited.remove(object_id)





    # =========================================================
    # SQLALCHEMY ROW → DICT
    # =========================================================

    @classmethod
    def _row_to_dict(
        cls,
        row: Any,
        visited: set[int] | None = None,
    ) -> dict:

        if not hasattr(row, "_mapping"):
            return row

        return {
            key: cls._normalize(
                value,
                visited=visited,
            )
            for key, value in row._mapping.items()
        }

    # =========================================================
    # NORMALIZE
    # =========================================================

    @classmethod
    def _normalize(
        cls,
        data: Any,
        visited: set[int] | None = None,
    ) -> Any:
        """
        Recursively normalize presentation data.

        Supported:

            dict
            SQLAlchemy ORM objects
            SQLAlchemy Rows
            list
            tuple
            scalar values
        """

        if visited is None:
            visited = set()

        if data is None:
            return None

        # ---------------------------------------------
        # Dictionary
        # ---------------------------------------------

        if isinstance(data, dict):

            return {
                key: cls._normalize(
                    value,
                    visited=visited,
                )
                for key, value in data.items()
            }

        # ---------------------------------------------
        # SQLAlchemy ORM object
        # ---------------------------------------------

        if hasattr(data, "__table__"):

            return cls._model_to_dict(
                data,
                visited=visited,
            )

        # ---------------------------------------------
        # SQLAlchemy Row
        # ---------------------------------------------

        if hasattr(data, "_mapping"):

            return cls._row_to_dict(
                data,
                visited=visited,
            )

        # ---------------------------------------------
        # List
        # ---------------------------------------------

        if isinstance(data, list):

            return [
                cls._normalize(
                    item,
                    visited=visited,
                )
                for item in data
            ]

        # ---------------------------------------------
        # Tuple
        # ---------------------------------------------

        if isinstance(data, tuple):

            return [
                cls._normalize(
                    item,
                    visited=visited,
                )
                for item in data
            ]

        # ---------------------------------------------
        # Scalar
        # ---------------------------------------------

        return data

    # =========================================================
    # PRESENT VALUE
    # =========================================================

    async def present(
        self,
        value: Any,
    ) -> Any:

        if value is None:
            return None

        ready = await self._ensure_setup()

        if not ready:
            return value

        return await self._pipeline.transform(
            value=value,
            context=self._settings_context,
        )

    # =========================================================
    # PRESENT RECORD
    # =========================================================


    async def present_record(
        self,
        record: Any,
        money_fields: set[str] | list[str] | None = None,
    ) -> dict:

        record = self._normalize(record)

        if record is None:
            return None

        if not isinstance(record, dict):
            return await self.present(record)

        ready = await self._ensure_setup()

        if not ready:
            return record

        money_fields = set(money_fields or [])
        return await self._present_recursive(
            record,
            money_fields=money_fields,
        )

    # =========================================================
    # PRESENT RECURSIVELY
    # =========================================================

    async def _present_recursive(
        self,
        value: Any,
        money_fields: set[str] | None = None,
        field_name: str | None = None,
        currency: str | None = None,
    ) -> Any:

        money_fields = money_fields or set()

        if value is None:
            return None

        # =====================================================
        # DICT
        # =====================================================

        if isinstance(value, dict):

            current_currency = value.get("currency") or currency

            return {
                key: await self._present_recursive(
                    item,
                    money_fields=money_fields,
                    field_name=key,
                    currency=current_currency,
                )
                for key, item in value.items()
            }

        # =====================================================
        # LIST
        # =====================================================

        if isinstance(value, list):

            return [
                await self._present_recursive(
                    item,
                    money_fields=money_fields,
                    field_name=field_name,
                    currency=currency,
                )
                for item in value
            ]

        # =====================================================
        # TUPLE
        # =====================================================

        if isinstance(value, tuple):

            return [
                await self._present_recursive(
                    item,
                    money_fields=money_fields,
                    field_name=field_name,
                    currency=currency,
                )
                for item in value
            ]

        # =====================================================
        # MONEY
        # =====================================================

        if (
            field_name in money_fields
            and isinstance(value, Decimal)
            and currency
        ):
            return await self._pipeline.transform_currency(
                value=value,
                currency=currency,
                context=self._settings_context,
            )

        # =====================================================
        # OTHER SCALARS
        # =====================================================

        return await self._pipeline.transform(
            value=value,
            context=self._settings_context,
        )

    # =========================================================
    # PRESENT RECORDS
    # =========================================================

    async def present_records(
        self,
        records: Any,
        money_fields: set[str] | list[str] | tuple[str, ...] | None = None,
    ) -> list:

        records = self._normalize(records)

        if records is None:
            return []

        if not isinstance(records, list):
            records = [records]

        ready = await self._ensure_setup()

        if not ready:
            return records

        money_fields = set(money_fields or [])

        return [
            await self.present_record(
                record,
                money_fields=money_fields,
            )
            for record in records
        ]