from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from datetime import datetime


class EmailCreate(BaseModel):

    source_module: str | None = None

    entity_type: str | None = Field(
        default=None,
        max_length=100,
    )

    entity_id: UUID | None = None

    email_type: str | None = None

    priority: str | None = None

    from_email: EmailStr | None = None

    from_name: str | None = Field(
        default=None,
        max_length=255,
    )

    reply_to: EmailStr | None = None

    subject: str = Field(
        min_length=1,
        max_length=500,
    )

    body_html: str | None = None

    body_text: str | None = None

    template_id: UUID | None = None

    template_version_id: UUID | None = None

    template_variables: dict | None = None

    recipients: list[dict] = Field(
        min_length=1,
    )

    attachments: list[dict] = Field(
        default_factory=list,
    )




class EmailResponse(BaseModel):

    id: UUID

    tenant_id: UUID

    company_id: UUID

    branch_id: UUID

    email_number: str

    message_id: str | None = None

    thread_id: str | None = None

    source_module: str | None = None

    entity_type: str | None = None

    entity_id: UUID | None = None

    email_type: str | None = None

    status: str | None = None

    priority: str | None = None

    from_email: EmailStr

    from_name: str | None = None

    reply_to: EmailStr | None = None

    subject: str

    body_html: str | None = None

    body_text: str | None = None

    template_id: UUID | None = None

    template_version_id: UUID | None = None

    template_variables: dict | None = None

    attachment_count: int

    attempts: int

    max_attempts: int

    sent_at: datetime | None = None

    failed_at: datetime | None = None

    error_message: str | None = None

    is_system: bool

    is_archived: bool

    model_config = {
        "from_attributes": True,
    }


class EmailListItem(BaseModel):

    id: UUID

    email_number: str

    source_module: str | None = None

    email_type: str | None = None

    status: str | None = None

    priority: str | None = None

    from_email: EmailStr

    subject: str

    attachment_count: int

    attempts: int

    sent_at: datetime | None = None

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }