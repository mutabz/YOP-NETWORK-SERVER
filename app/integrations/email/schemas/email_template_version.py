from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

# ============================================================
# CREATE VERSION
# ============================================================

class EmailTemplateVersionCreate(BaseModel):

    template_id: UUID

    subject_template: str = Field(
        min_length=1,
        max_length=500,
    )

    html_template: str = Field(
        min_length=1,
    )

    text_template: str | None = None

    variables: dict | None = None

    changelog: str | None = Field(
        default=None,
        max_length=2000,
    )


# ============================================================
# RESPONSE
# ============================================================

class EmailTemplateVersionResponse(BaseModel):

    id: UUID

    template_id: UUID

    version: int

    source_module: str | None = None

    email_type: str | None = None

    subject_template: str

    html_template: str

    text_template: str | None

    variables: dict | None

    checksum: str | None

    changelog: str | None

    published: bool

    published_at: datetime | None

    created_at: datetime

    updated_at: datetime | None

    model_config = {
        "from_attributes": True,
    }


# ============================================================
# LIST ITEM
# ============================================================

class EmailTemplateVersionListItem(BaseModel):

    id: UUID

    template_id: UUID

    version: int

    checksum: str | None

    changelog: str | None

    published: bool

    published_at: datetime | None

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }