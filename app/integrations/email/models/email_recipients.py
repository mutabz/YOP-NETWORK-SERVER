from __future__ import annotations

import uuid

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_model import BaseModelSys

from app.integrations.email.enums import (
    EmailRecipientType
)


class EmailRecipient(BaseModelSys):

    __tablename__ = "system_email_recipients"


    email_id: Mapped[uuid.UUID] = mapped_column( UUID(as_uuid=True), ForeignKey( "system_emails.id", ondelete="CASCADE", ), nullable=False, index=True, )
    recipient_type: Mapped[EmailRecipientType] = mapped_column( Enum(EmailRecipientType), nullable=False, index=True, )
    email: Mapped[str] = mapped_column( String(320), nullable=False, index=True, )
    name: Mapped[str | None] = mapped_column( String(255), )
    user_id: Mapped[uuid.UUID | None] = mapped_column( UUID(as_uuid=True), index=True, )
    delivered: Mapped[bool | None] = mapped_column( Boolean, )