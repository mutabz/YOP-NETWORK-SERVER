from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, DateTime, Enum, Integer,
    String, Text, JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_model import BaseModelSys

from app.integrations.email.enums import (
    EmailPriority,
    EmailProvider,
    EmailSourceModule,
    EmailStatus,
    EmailType,
)


class Email(BaseModelSys):

    __tablename__ = "system_emails"


    tenant_id: Mapped[uuid.UUID] = mapped_column( UUID(as_uuid=True), nullable=False, index=True, )
    company_id: Mapped[uuid.UUID] = mapped_column( UUID(as_uuid=True), nullable=False, index=True, )
    branch_id: Mapped[uuid.UUID] = mapped_column( UUID(as_uuid=True), nullable=False, index=True, )

    email_number: Mapped[str] = mapped_column( String(100), nullable=False, unique=True, index=True, )
    message_id: Mapped[str | None] = mapped_column( String(255), index=True, )
    thread_id: Mapped[str | None] = mapped_column( String(255), index=True, )

    source_module: Mapped[EmailSourceModule] = mapped_column( Enum(EmailSourceModule), nullable=False, index=True, )
    entity_type: Mapped[str | None] = mapped_column( String(100), index=True, )
    entity_id: Mapped[uuid.UUID | None] = mapped_column( UUID(as_uuid=True), index=True, )
    email_type: Mapped[EmailType] = mapped_column( Enum(EmailType), nullable=False, index=True, )

    status: Mapped[EmailStatus] = mapped_column( Enum(EmailStatus), default=EmailStatus.DRAFT, nullable=False, index=True, )
    priority: Mapped[EmailPriority] = mapped_column( Enum(EmailPriority), default=EmailPriority.NORMAL, nullable=False, index=True, )
    provider: Mapped[EmailProvider] = mapped_column( Enum(EmailProvider), default=EmailProvider.GMAIL, nullable=False, )

    from_email: Mapped[str] = mapped_column( String(320), nullable=False, )
    from_name: Mapped[str | None] = mapped_column( String(255), )
    reply_to: Mapped[str | None] = mapped_column( String(320), )

    subject: Mapped[str] = mapped_column( String(500), nullable=False, )
    body_html: Mapped[str | None] = mapped_column( Text, )
    body_text: Mapped[str | None] = mapped_column( Text, )

    template_id: Mapped[uuid.UUID | None] = mapped_column( UUID(as_uuid=True), index=True, )
    template_version_id: Mapped[uuid.UUID | None] = mapped_column( UUID(as_uuid=True), index=True, )
    template_variables: Mapped[dict | None] = mapped_column( JSON, )

    attachment_count: Mapped[int] = mapped_column( Integer, default=0, nullable=False, )

    attempts: Mapped[int] = mapped_column( Integer, default=0, nullable=False, )
    max_attempts: Mapped[int] = mapped_column( Integer, default=3, nullable=False, )

    sent_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), )
    failed_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), )
    error_message: Mapped[str | None] = mapped_column( String(4000), )

    extra_metadata: Mapped[dict | None] = mapped_column( JSON, )
    is_system: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False, )
    is_archived: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False, )

