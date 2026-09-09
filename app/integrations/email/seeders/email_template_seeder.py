from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID
import hashlib
import re

import yaml

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.email.enums import (
    EmailSourceModule,
    EmailType,
    EmailTemplateCode,
)

from app.integrations.email.models import (
    EmailTemplate,
    EmailTemplateVersion,
)


class EmailTemplateSeeder:

    def __init__(
        self,
    ):
        self.templates_path = (
            Path(__file__).parent.parent / "templates"
        )

    # =========================================================
    # SEED ALL
    # =========================================================

    async def seed(
        self,
        session,
        company,
    ) -> None:

        if not self.templates_path.exists():
            print(
                f"⚠️ Email templates directory does not exist: "
                f"{self.templates_path}"
            )
            return

        template_files = sorted(
            self.templates_path.glob("*.html")
        )

        if not template_files:
            print(
                "ℹ️ No email templates found."
            )
            return

        seeded = 0
        skipped = 0

        for template_file in template_files:

            try:

                created = await self.seed_file(
                    session=session,
                    template_file=template_file,
                    tenant_id=company.tenant_id,
                    company_id=company.id,
                )

                if created:
                    seeded += 1
                else:
                    skipped += 1

            except Exception as exc:

                print(
                    f"❌ Failed to seed email template "
                    f"{template_file.name}: {exc}"
                )

                raise

        await session.commit()

        print(
            f"✅ Email templates seeded: "
            f"{seeded} created, {skipped} skipped."
        )

    # =========================================================
    # SEED SINGLE FILE
    # =========================================================

    async def seed_file(
        self,
        *,
        session,
        template_file: Path,
        tenant_id: UUID,
        company_id: UUID,
    ) -> bool:

        content = template_file.read_text(
            encoding="utf-8"
        )

        extra_metadata, html_template = (
            self._parse_template(content)
        )

        code = extra_metadata.get("code")

        if not code:
            raise ValueError(
                f"Template '{template_file.name}' "
                f"does not define a code."
            )

        # =====================================================
        # CHECK EXISTING TEMPLATE
        # =====================================================

        existing = await session.scalar(
            select(EmailTemplate)
            .where(
                EmailTemplate.code == code
            )
        )

        if existing:
            print(
                f"⏭️ Email template already exists: {code}"
            )
            return False

        # =====================================================
        # METADATA
        # =====================================================

        name = extra_metadata.get(
            "name",
            template_file.stem.replace("_", " ").title(),
        )

        description = extra_metadata.get(
            "description"
        )

        source_module = EmailSourceModule(
            extra_metadata["source_module"]
        )

        email_type = EmailType(
            extra_metadata["email_type"]
        )

        subject_template = extra_metadata.get(
            "subject"
        )

        if not subject_template:
            raise ValueError(
                f"Template '{code}' "
                f"does not define a subject."
            )

        variables = extra_metadata.get(
            "variables",
            {},
        )

        category = extra_metadata.get(
            "category"
        )

        tags = extra_metadata.get(
            "tags",
            {},
        )

        # =====================================================
        # CHECKSUM
        # =====================================================

        checksum = hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()

        # =====================================================
        # CREATE TEMPLATE
        # =====================================================

        template = EmailTemplate(

            tenant_id=tenant_id,
            company_id=company_id,

            name=name,
            code=EmailTemplateCode(code),

            description=description,

            source_module=source_module,
            email_type=email_type,

            version=1,

            subject_template=subject_template,
            html_template=html_template,
            text_template=None,

            variables=variables,

            author="ERP System",
            category=category,
            tags=tags,

            is_default=True,
            is_system=True,
            is_active=True,
            is_public=False,

            published_at=datetime.now(
                timezone.utc
            ),
        )

        session.add(
            template
        )

        await session.flush()

        # =====================================================
        # CREATE VERSION
        # =====================================================

        version = EmailTemplateVersion(

            template_id=template.id,

            version=1,

            source_module=source_module,
            email_type=email_type,

            subject_template=subject_template,
            html_template=html_template,
            text_template=None,

            variables=variables,

            checksum=checksum,

            changelog="Initial system email template.",

            published=True,
        )

        session.add(
            version
        )

        print(
            f"✅ Email template seeded: {code}"
        )

        return True

    # =========================================================
    # PARSE TEMPLATE
    # =========================================================

    def _parse_template(
        self,
        content: str,
    ) -> tuple[dict, str]:

        match = re.match(
            r"^\s*<!--\s*(.*?)\s*-->\s*(.*)$",
            content,
            re.DOTALL,
        )

        if not match:
            raise ValueError(
                "Template must contain a extra_metadata "
                "comment at the beginning."
            )

        extra_metadata_raw = match.group(1)
        html_template = match.group(2)

        extra_metadata = yaml.safe_load(
            extra_metadata_raw
        )

        if not isinstance(extra_metadata, dict):
            raise ValueError(
                "Template extra_metadata must be a YAML object."
            )

        return extra_metadata, html_template