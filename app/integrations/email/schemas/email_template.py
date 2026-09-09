from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


# ============================================================
# CREATE
# ============================================================

class EmailTemplateCreate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=150,
    )

    code: str = Field(
        min_length=1,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    source_module: str | None = None

    email_type: str | None = None

    subject_template: str = Field(
        min_length=1,
        max_length=500,
    )

    html_template: str = Field(
        min_length=1,
    )

    text_template: str | None = None

    variables: dict | None = None

    category: str | None = Field(
        default=None,
        max_length=100,
    )

    tags: dict | None = None

    is_default: bool = False

    is_public: bool = False


# ============================================================
# UPDATE
# ============================================================

class EmailTemplateUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    subject_template: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
    )

    html_template: str | None = None

    text_template: str | None = None

    variables: dict | None = None

    category: str | None = Field(
        default=None,
        max_length=100,
    )

    tags: dict | None = None

    is_default: bool | None = None

    is_public: bool | None = None

    is_active: bool | None = None


# ============================================================
# PUBLISH
# ============================================================

class EmailTemplatePublishRequest(BaseModel):

    version: int | None = Field(
        default=None,
        ge=1,
    )


# ============================================================
# RESPONSE
# ============================================================

class EmailTemplateResponse(BaseModel):

    id: UUID

    tenant_id: UUID

    company_id: UUID

    branch_id: UUID

    name: str

    code: str

    description: str | None

    source_module: str | None = None

    email_type: str | None = None

    version: int

    subject_template: str

    html_template: str

    text_template: str | None

    variables: dict | None

    category: str | None

    tags: dict | None

    is_default: bool

    is_system: bool

    is_public: bool

    is_active: bool

    published_at: datetime | None

    created_at: datetime

    updated_at: datetime | None

    model_config = {
        "from_attributes": True,
    }


# ============================================================
# LIST ITEM
# ============================================================

class EmailTemplateListItem(BaseModel):

    id: UUID

    name: str

    code: str

    source_module: str | None = None

    email_type: str | None = None

    version: int

    category: str | None

    is_default: bool

    is_system: bool

    is_public: bool

    is_active: bool

    published_at: datetime | None

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }