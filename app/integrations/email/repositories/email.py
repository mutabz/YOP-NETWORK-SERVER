from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from app.shared.base_repository import BaseRepository

from app.integrations.email.models import Email
from app.integrations.email.enums import EmailStatus


class EmailRepository(BaseRepository):

    model = Email

    # =========================
    # EMAIL LOOKUPS
    # =========================

    async def get_by_number(
        self,
        email_number: str,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "email_number": email_number,
            },
            select_fields=select_fields,
        )


    async def get_by_message_id(
        self,
        message_id: str,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "message_id": message_id,
            },
            select_fields=select_fields,
        )


    async def get_by_thread_id(
        self,
        thread_id: str,
        select_fields=None,
    ):
        return await self.find(
            filters={
                "thread_id": thread_id,
            },
            select_fields=select_fields,
        )


    # =========================
    # STATUS
    # =========================

    async def update_status(
        self,
        email_id: UUID,
        status: EmailStatus,
    ):
        return await self.update(
            email_id,
            status=status,
        )


    async def mark_sent(
        self,
        email_id: UUID,
        sent_at: datetime | None = None,
    ):
        return await self.update(
            email_id,
            status=EmailStatus.SENT,
            sent_at=sent_at or datetime.now(timezone.utc),
            error_message=None,
        )


    async def mark_failed(
        self,
        email_id: UUID,
        error_message: str,
        failed_at: datetime | None = None,
    ):
        return await self.update(
            email_id,
            status=EmailStatus.FAILED,
            failed_at=failed_at or datetime.now(timezone.utc),
            error_message=error_message,
        )


    async def mark_sending(
        self,
        email_id: UUID,
    ):
        return await self.update(
            email_id,
            status=EmailStatus.SENDING,
        )


    async def mark_cancelled(
        self,
        email_id: UUID,
    ):
        return await self.update(
            email_id,
            status=EmailStatus.CANCELLED,
        )


    # =========================
    # ATTEMPTS
    # =========================

    async def increment_attempts(
        self,
        email_id: UUID,
    ):
        email = await self.get(email_id)

        if not email:
            return None

        return await self.update(
            email_id,
            attempts=email.attempts + 1,
        )


    # =========================
    # EMAIL HISTORY
    # =========================

    async def get_sent(
        self,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "status": EmailStatus.SENT,
            },
            sort_by="sent_at",
            direction="desc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )


    async def get_failed(
        self,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "status": EmailStatus.FAILED,
            },
            sort_by="failed_at",
            direction="desc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )


    async def get_pending(
        self,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "status": EmailStatus.PENDING,
            },
            sort_by="created_at",
            direction="asc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )

