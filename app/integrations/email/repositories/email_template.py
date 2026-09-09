from __future__ import annotations

from uuid import UUID

from app.shared.base_repository import BaseRepository

from app.integrations.email.models import EmailTemplate
from app.integrations.email.enums import (
    EmailSourceModule, EmailType
)


class EmailTemplateRepository(BaseRepository):

    model = EmailTemplate

    # =========================
    # LOOKUPS
    # =========================

    async def get_by_code(
        self,
        code: str,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "code": code,
            },
            select_fields=select_fields,
        )


    async def get_active_by_code(
        self,
        code: str,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "code": code,
                "is_active": True,
            },
            select_fields=select_fields,
        )


    # =========================
    # DEFAULT TEMPLATE
    # =========================

    async def get_default(
        self,
        source_module: EmailSourceModule,
        email_type: EmailType,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "source_module": source_module,
                "email_type": email_type,
                "is_default": True,
                "is_active": True,
            },
            select_fields=select_fields,
        )


    # =========================
    # ACTIVE TEMPLATES
    # =========================

    async def get_active(
        self,
        source_module: EmailSourceModule | None = None,
        email_type: EmailType | None = None,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        filters = {
            "is_active": True,
        }

        if source_module is not None:
            filters["source_module"] = source_module

        if email_type is not None:
            filters["email_type"] = email_type

        return await self.list(
            filters=filters,
            sort_by="name",
            direction="asc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )


    # =========================
    # SOURCE MODULE
    # =========================

    async def get_by_source_module(
        self,
        source_module: EmailSourceModule,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "source_module": source_module,
            },
            sort_by="name",
            direction="asc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )


    # =========================
    # EMAIL TYPE
    # =========================

    async def get_by_email_type(
        self,
        email_type: EmailType,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "email_type": email_type,
            },
            sort_by="name",
            direction="asc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )


    # =========================
    # SYSTEM TEMPLATES
    # =========================

    async def get_system_templates(
        self,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "is_system": True,
                "is_active": True,
            },
            sort_by="name",
            direction="asc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )


    # =========================
    # PUBLIC TEMPLATES
    # =========================

    async def get_public_templates(
        self,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "is_public": True,
                "is_active": True,
            },
            sort_by="name",
            direction="asc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )