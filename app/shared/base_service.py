from app.shared.managers.realtime_manager import RealtimeManager
from app.shared.managers.workflow_manager import WorkflowManager

from app.shared.query_engine import to_json

import datetime
import uuid

from pydantic import ValidationError


class BaseService:

    model_name = "unknown"

    create_schema = None
    update_schema = None

    def __init__(self, repository):
        self.repository = repository

    def to_json(self, obj):

        if isinstance(obj, uuid.UUID):
            return str(obj)

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        if isinstance(obj, dict):
            return {
                key: self.to_json(value)
                for key, value in obj.items()
            }

        if isinstance(obj, (list, tuple, set)):
            return [
                self.to_json(item)
                for item in obj
            ]

        if hasattr(obj, "__table__"):
            return {
                c.name: to_json(getattr(obj, c.name))
                for c in obj.__table__.columns
            }

        return obj

    # =====================================
    # VALIDATION
    # =====================================

    async def validate_create(self, data: dict):

        if not self.create_schema:
            return data

        try:
            validated = self.create_schema(**data)
            return validated.model_dump()

        except ValidationError as e:
            raise ValueError(e.errors())

    async def validate_update(self, data: dict):

        if not self.update_schema:
            return data

        try:
            validated = self.update_schema(**data)
            return validated.model_dump(
                exclude_unset=True
            )

        except ValidationError as e:
            raise ValueError(e.errors())

    # =====================================
    # BUSINESS VALIDATION
    # =====================================

    async def validate_business_create(self, data: dict):
        return data

    async def validate_business_update(
        self,
        id_,
        data: dict
    ):
        return data

    async def validate_business_delete(self, id_):
        return

    # =====================================
    # BEFORE HOOKS
    # =====================================

    async def before_create(self, data: dict):
        return data

    async def before_update(
        self,
        id_,
        data: dict
    ):
        return data

    async def before_delete(self, id_):
        return

    # =====================================
    # RECORD ID
    # =====================================

    def _resolve_record_id(self, obj):

        if obj is None:
            return None

        for attribute in (
            "id",
            "uuid",
            "code",
        ):
            value = getattr(
                obj,
                attribute,
                None
            )

            if value not in (None, ""):
                return value

        return None

    # =====================================
    # CREATE
    # =====================================

    async def create(self, **data):

        data = await self.before_create(data)

        data = await self.validate_create(data)

        data = await self.validate_business_create(data)

        obj = await self.repository.create(**data)

        await self.after_create(obj)

        return obj

    # =====================================
    # FAST CREATE
    # =====================================

    async def fast_create(self, **data):

        data = await self.before_create(data)

        data = await self.validate_create(data)

        data = await self.validate_business_create(data)

        obj = await self.repository.fast_create(**data)

        await self.after_create(obj)

        return obj

    # =====================================
    # BULK CREATE
    # =====================================

    async def bulk_create(self, data):

        data = await self.before_create(data)

        data = await self.validate_create(data)

        data = await self.validate_business_create(data)

        obj = await self.repository.bulk_create(data)

        return obj

    # =====================================
    # UPDATE
    # =====================================

    async def update(self, id_, **data):

        data = await self.before_update(
            id_,
            data
        )

        data = await self.validate_update(data)

        data = await self.validate_business_update(
            id_,
            data
        )

        obj = await self.repository.update(
            id_,
            **data
        )

        await self.after_update(obj)

        return obj

    # =====================================
    # FAST UPDATE
    # =====================================

    async def fast_update(self, id_, **data):

        data = await self.before_update(
            id_,
            data
        )

        data = await self.validate_update(data)

        data = await self.validate_business_update(
            id_,
            data
        )

        obj = await self.repository.fast_update(
            id_,
            **data
        )

        return obj

    # =====================================
    # DELETE
    # =====================================

    async def delete(self, id_):

        await self.before_delete(id_)

        await self.validate_business_delete(id_)

        result = await self.repository.delete(id_)

        if result:
            await self.after_delete(id_)

        return result

    # =====================================
    # AFTER CREATE
    # =====================================

    async def after_create(self, obj):

        action = f"{self.model_name}.created"

        record_id = self._resolve_record_id(obj)

        if obj:

            try:
                await WorkflowManager.publish(
                    event_type=action,
                    payload={
                        "model": self.model_name,
                        "action": action,
                        "record_id": (
                            str(record_id)
                            if record_id is not None
                            else ""
                        ),
                    },
                )

            except Exception as e:
                print(e, obj)

    # =====================================
    # AFTER UPDATE
    # =====================================

    async def after_update(self, obj):

        action = f"{self.model_name}.updated"

        record_id = self._resolve_record_id(obj)

        if obj:

            try:

                await WorkflowManager.publish(
                    event_type=action,
                    payload={
                        "model": self.model_name,
                        "action": action,
                        "record_id": (
                            str(record_id)
                            if record_id is not None
                            else ""
                        ),
                    },
                )

            except Exception as e:
                print(e)

    # =====================================
    # AFTER DELETE
    # =====================================

    async def after_delete(self, id_):

        action = f"{self.model_name}.deleted"

        try:
            
            await WorkflowManager.publish(
                event_type=action,
                payload={
                    "model": self.model_name,
                    "action": action,
                    "record_id": str(id_),
                },
            )

        except Exception:
            return id_

    # =====================================
    # READ
    # =====================================

    async def get(self, id_):
        return await self.repository.get(id_)

    async def get_all(self):
        return await self.repository.all()

    async def count(self):
        return await self.repository.count()