from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field




class EmailRecipientCreate(BaseModel):

    email: EmailStr

    name: str | None = Field(
        default=None,
        max_length=255,
    )

    recipient_type: str | None = None 

    user_id: UUID | None = None


class EmailRecipientResponse(BaseModel):

    id: UUID

    email_id: UUID

    recipient_type: str | None = None

    email: EmailStr

    name: str | None = None

    user_id: UUID | None = None

    delivered: bool | None = None

    model_config = {
        "from_attributes": True,
    }


