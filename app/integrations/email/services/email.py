from __future__ import annotations

from uuid import UUID

from app.shared.base_service import BaseService

from app.integrations.email.repositories import (
    EmailRepository,
)

from app.integrations.email.enums import (
    EmailStatus,
)


class EmailService(BaseService):

    model_name = "email"

    create_schema = None
    update_schema = None

    def __init__(
        self,
        repository: EmailRepository,
    ):
        super().__init__(repository)

        self.repository: EmailRepository = repository

    # =========================================================
    # LOOKUPS
    # =========================================================

    async def get_by_number(
        self,
        email_number: str,
        select_fields=None,
    ):
        return await self.repository.get_by_number(
            email_number=email_number,
            select_fields=select_fields,
        )

    async def get_by_message_id(
        self,
        message_id: str,
        select_fields=None,
    ):
        return await self.repository.get_by_message_id(
            message_id=message_id,
            select_fields=select_fields,
        )

    async def get_by_thread_id(
        self,
        thread_id: str,
        select_fields=None,
    ):
        return await self.repository.get_by_thread_id(
            thread_id=thread_id,
            select_fields=select_fields,
        )

    # =========================================================
    # STATUS
    # =========================================================

    async def update_status(
        self,
        email_id: UUID,
        status: EmailStatus,
    ):
        return await self.repository.update_status(
            email_id=email_id,
            status=status,
        )

    async def mark_sending(
        self,
        email_id: UUID,
    ):
        return await self.repository.mark_sending(
            email_id=email_id,
        )

    async def mark_sent(
        self,
        email_id: UUID,
    ):
        return await self.repository.mark_sent(
            email_id=email_id,
        )

    async def mark_failed(
        self,
        email_id: UUID,
        error_message: str,
    ):
        return await self.repository.mark_failed(
            email_id=email_id,
            error_message=error_message,
        )

    async def mark_cancelled(
        self,
        email_id: UUID,
    ):
        return await self.repository.mark_cancelled(
            email_id=email_id,
        )

    # =========================================================
    # ATTEMPTS
    # =========================================================

    async def increment_attempts(
        self,
        email_id: UUID,
    ):
        return await self.repository.increment_attempts(
            email_id=email_id,
        )

    # =========================================================
    # HISTORY
    # =========================================================

    async def get_sent(
        self,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.repository.get_sent(
            select_fields=select_fields,
            page=page,
            per_page=per_page,
        )

    async def get_failed(
        self,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.repository.get_failed(
            select_fields=select_fields,
            page=page,
            per_page=per_page,
        )

    async def get_pending(
        self,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.repository.get_pending(
            select_fields=select_fields,
            page=page,
            per_page=per_page,
        )