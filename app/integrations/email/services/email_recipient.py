from __future__ import annotations

from uuid import UUID

from app.shared.base_service import BaseService

from app.integrations.email.repositories import (
    EmailRecipientRepository,
)


class EmailRecipientService(BaseService):

    model_name = "email_recipient"

    create_schema = None

    def __init__(
        self,
        repository: EmailRecipientRepository,
    ):
        super().__init__(repository)

        self.repository: EmailRecipientRepository = repository

    # =========================================================
    # EMAIL RECIPIENTS
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

    async def get_by_type(
        self,
        email_id: UUID,
        recipient_type,
        select_fields=None,
    ):
        return await self.repository.get_by_type(
            email_id=email_id,
            recipient_type=recipient_type,
            select_fields=select_fields,
        )

    # =========================================================
    # LOOKUP
    # =========================================================

    async def get_by_address(
        self,
        email_id: UUID,
        address: str,
        select_fields=None,
    ):
        return await self.repository.get_by_address(
            email_id=email_id,
            address=address,
            select_fields=select_fields,
        )