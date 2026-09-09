from __future__ import annotations

from uuid import UUID

from app.shared.base_service import BaseService

from app.integrations.email.repositories import (
    EmailTemplateRepository,
)

class EmailTemplateService(BaseService):

    model_name = "email_template"

    create_schema = None
    update_schema = None

    def __init__(
        self,
        repository: EmailTemplateRepository,
    ):
        super().__init__(repository)

        self.repository: EmailTemplateRepository = repository

    # =========================================================
    # LOOKUPS
    # =========================================================

    async def get_by_code(
        self,
        code: str,
        select_fields=None,
    ):
        return await self.repository.get_by_code(
            code=code,
            select_fields=select_fields,
        )

    async def get_default(
        self,
        select_fields=None,
    ):
        return await self.repository.get_default(
            select_fields=select_fields,
        )

    # =========================================================
    # STATUS
    # =========================================================

    async def publish(
        self,
        template_id: UUID,
    ):
        return await self.repository.publish(
            template_id=template_id,
        )

    async def unpublish(
        self,
        template_id: UUID,
    ):
        return await self.repository.unpublish(
            template_id=template_id,
        )

    # =========================================================
    # VERSIONS
    # =========================================================

    async def increment_version(
        self,
        template_id: UUID,
    ):
        return await self.repository.increment_version(
            template_id=template_id,
        )

    # =========================================================
    # BUSINESS VALIDATION
    # =========================================================

    async def validate_business_create(
        self,
        data: dict,
    ):
        code = data.get("code")

        if code:
            existing = await self.repository.get_by_code(
                code=code,
            )

            if existing:
                raise ValueError(
                    f"Email template with code '{code}' already exists."
                )

        return data

    async def validate_business_update(
        self,
        id_,
        data: dict,
    ):
        return data