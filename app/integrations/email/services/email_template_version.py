from __future__ import annotations

from uuid import UUID

from app.shared.base_service import BaseService

from app.integrations.email.repositories import (
    EmailTemplateVersionRepository,
)


class EmailTemplateVersionService(BaseService):

    model_name = "email_template_version"

    create_schema = None

    def __init__(
        self,
        repository: EmailTemplateVersionRepository,
    ):
        super().__init__(repository)

        self.repository: EmailTemplateVersionRepository = repository

    # =========================================================
    # LOOKUPS
    # =========================================================

    async def get_by_template(
        self,
        template_id: UUID,
        select_fields=None,
    ):
        return await self.repository.get_by_template(
            template_id=template_id,
            select_fields=select_fields,
        )

    async def get_version(
        self,
        template_id: UUID,
        version: int,
        select_fields=None,
    ):
        return await self.repository.get_version(
            template_id=template_id,
            version=version,
            select_fields=select_fields,
        )

    async def get_published(
        self,
        template_id: UUID,
        select_fields=None,
    ):
        return await self.repository.get_published(
            template_id=template_id,
            select_fields=select_fields,
        )

    # =========================================================
    # CHECKSUM
    # =========================================================

    async def get_by_checksum(
        self,
        checksum: str,
        select_fields=None,
    ):
        return await self.repository.get_by_checksum(
            checksum=checksum,
            select_fields=select_fields,
        )

    # =========================================================
    # STATUS
    # =========================================================

    async def publish(
        self,
        version_id: UUID,
    ):
        return await self.repository.publish(
            version_id=version_id,
        )

    async def unpublish(
        self,
        version_id: UUID,
    ):
        return await self.repository.unpublish(
            version_id=version_id,
        )

    # =========================================================
    # BUSINESS VALIDATION
    # =========================================================

    async def validate_business_create(
        self,
        data: dict,
    ):
        template_id = data.get("template_id")

        if not template_id:
            raise ValueError(
                "template_id is required."
            )

        return data