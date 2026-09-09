from __future__ import annotations

from app.shared.base_repository import BaseRepository

from app.integrations.email.models import (
    EmailAttachment,
)


class EmailAttachmentRepository(BaseRepository):

    model = EmailAttachment

    # =========================
    # EMAIL ATTACHMENTS
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
    # DOCUMENT
    # =========================

    async def get_by_document(
        self,
        document_id,
        select_fields=None,
        page: int = 1,
        per_page: int = 100,
    ):
        return await self.list(
            filters={
                "document_id": document_id,
            },
            sort_by="created_at",
            direction="desc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )

    # =========================
    # DOCUMENT FILE
    # =========================

    async def get_by_document_file(
        self,
        document_file_id,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "document_file_id": document_file_id,
            },
            select_fields=select_fields,
        )

    # =========================
    # INLINE ATTACHMENTS
    # =========================

    async def get_inline(
        self,
        email_id,
        select_fields=None,
    ):
        return await self.find(
            filters={
                "email_id": email_id,
                "is_inline": True,
            },
            select_fields=select_fields,
        )

    # =========================
    # REGULAR ATTACHMENTS
    # =========================

    async def get_regular(
        self,
        email_id,
        select_fields=None,
    ):
        return await self.find(
            filters={
                "email_id": email_id,
                "is_inline": False,
            },
            select_fields=select_fields,
        )

    # =========================
    # CONTENT ID
    # =========================

    async def get_by_content_id(
        self,
        email_id,
        content_id: str,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "email_id": email_id,
                "content_id": content_id,
            },
            select_fields=select_fields,
        )