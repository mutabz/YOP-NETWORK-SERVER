from __future__ import annotations

from app.shared.base_repository import BaseRepository

from app.integrations.email.models import (
    EmailTemplateVersion,
)


class EmailTemplateVersionRepository(BaseRepository):

    model = EmailTemplateVersion

    # =========================
    # TEMPLATE VERSIONS
    # =========================

    async def get_by_template(
        self,
        template_id,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "template_id": template_id,
            },
            sort_by="version",
            direction="desc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )


    async def get_version(
        self,
        template_id,
        version: int,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "template_id": template_id,
                "version": version,
            },
            select_fields=select_fields,
        )


    async def get_latest(
        self,
        template_id,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "template_id": template_id,
            },
            sort_by="version",
            direction="desc",
            select_fields=select_fields,
        )


    async def get_published(
        self,
        template_id,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "template_id": template_id,
                "published": True,
            },
            sort_by="version",
            direction="desc",
            select_fields=select_fields,
        )


    async def get_published_versions(
        self,
        template_id,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "template_id": template_id,
                "published": True,
            },
            sort_by="version",
            direction="desc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )