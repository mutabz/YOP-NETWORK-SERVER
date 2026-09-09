from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class EmailAttachmentCreate(BaseModel):

    document_id: UUID | None = None

    document_file_id: UUID | None = None

    filename: str = Field(
        min_length=1,
        max_length=255,
    )

    mime_type: str = Field(
        min_length=1,
        max_length=150,
    )

    file_size: int = Field(
        default=0,
        ge=0,
    )

    is_inline: bool = False

    content_id: str | None = Field(
        default=None,
        max_length=255,
    )


class EmailAttachmentResponse(BaseModel):

    id: UUID

    email_id: UUID

    document_id: UUID | None = None

    document_file_id: UUID | None = None

    filename: str

    mime_type: str

    file_size: int

    is_inline: bool

    content_id: str | None = None

    model_config = {
        "from_attributes": True,
    }