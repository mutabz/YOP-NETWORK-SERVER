from __future__ import annotations

from uuid import UUID

from app.shared.base_service import BaseService

from app.integrations.email.repositories import (
    EmailAttachmentRepository,
)


class EmailAttachmentService(BaseService):

    model_name = "email_attachment"

    create_schema = None

    def __init__(
        self,
        repository: EmailAttachmentRepository,
    ):
        super().__init__(repository)

        self.repository: EmailAttachmentRepository = repository

    # =========================================================
    # EMAIL ATTACHMENTS
    # =========================================================

    async def get_by_email(
        self,
        email_id: UUID,
        select_fields=None,
    ):
        return await self.repository.get_by_email(
            email_id=email_id,
            select_fields=select_fields,
        )

    # =========================================================
    # PRIMARY
    # =========================================================

    async def get_primary(
        self,
        email_id: UUID,
        select_fields=None,
    ):
        return await self.repository.get_primary(
            email_id=email_id,
            select_fields=select_fields,
        )

    # =========================================================
    # DOCUMENT
    # =========================================================

    async def get_by_document(
        self,
        document_id: UUID,
        select_fields=None,
    ):
        return await self.repository.get_by_document(
            document_id=document_id,
            select_fields=select_fields,
        )

    async def get_by_document_file(
        self,
        document_file_id: UUID,
        select_fields=None,
    ):
        return await self.repository.get_by_document_file(
            document_file_id=document_file_id,
            select_fields=select_fields,
        )