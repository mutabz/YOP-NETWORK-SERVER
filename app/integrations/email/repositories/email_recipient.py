from __future__ import annotations

from app.shared.base_repository import BaseRepository

from app.integrations.email.models import (
    EmailRecipient,
)

from app.integrations.email.enums import (
    EmailRecipientType,
)


class EmailRecipientRepository(BaseRepository):

    model = EmailRecipient

    # =========================
    # EMAIL RECIPIENTS
    # =========================

    async def get_by_email(
        self,
        email_id,
        select_fields=None,
        page: int = 1,
        per_page: int = 100,
    ):
        return await self.list(
            filters={
                "email_id": email_id,
            },
            sort_by="created_at",
            direction="asc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )

    # =========================
    # RECIPIENT TYPE
    # =========================

    async def get_by_type(
        self,
        email_id,
        recipient_type: EmailRecipientType,
        select_fields=None,
        page: int = 1,
        per_page: int = 100,
    ):
        return await self.list(
            filters={
                "email_id": email_id,
                "recipient_type": recipient_type,
            },
            sort_by="created_at",
            direction="asc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )

    # =========================
    # TO RECIPIENTS
    # =========================

    async def get_to_recipients(
        self,
        email_id,
        select_fields=None,
    ):
        return await self.find(
            filters={
                "email_id": email_id,
                "recipient_type": EmailRecipientType.TO,
            },
            select_fields=select_fields,
        )

    # =========================
    # CC RECIPIENTS
    # =========================

    async def get_cc_recipients(
        self,
        email_id,
        select_fields=None,
    ):
        return await self.find(
            filters={
                "email_id": email_id,
                "recipient_type": EmailRecipientType.CC,
            },
            select_fields=select_fields,
        )

    # =========================
    # BCC RECIPIENTS
    # =========================

    async def get_bcc_recipients(
        self,
        email_id,
        select_fields=None,
    ):
        return await self.find(
            filters={
                "email_id": email_id,
                "recipient_type": EmailRecipientType.BCC,
            },
            select_fields=select_fields,
        )

    # =========================
    # EMAIL ADDRESS
    # =========================

    async def get_by_address(
        self,
        email: str,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "email": email,
            },
            sort_by="created_at",
            direction="desc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )

    # =========================
    # USER
    # =========================

    async def get_by_user(
        self,
        user_id,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "user_id": user_id,
            },
            sort_by="created_at",
            direction="desc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )

    # =========================
    # DELIVERY
    # =========================

    async def mark_delivered(
        self,
        recipient_id,
    ):
        return await self.update(
            recipient_id,
            delivered=True,
        )

    async def mark_undelivered(
        self,
        recipient_id,
    ):
        return await self.update(
            recipient_id,
            delivered=False,
        )