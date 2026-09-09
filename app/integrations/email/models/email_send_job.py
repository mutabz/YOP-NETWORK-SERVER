from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime, Enum,
    Integer, JSON,
    String, ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_model import BaseModelSys

from app.integrations.email.enums import (
    EmailPriority,
    EmailSendJobStatus,
)


class EmailSendJob(BaseModelSys):

    __tablename__ = "system_email_send_jobs"


    email_id: Mapped[uuid.UUID] = mapped_column( UUID(as_uuid=True), ForeignKey( "system_emails.id", ondelete="CASCADE", ), nullable=False, index=True, )
    priority: Mapped[EmailPriority] = mapped_column( Enum(EmailPriority), default=EmailPriority.NORMAL, nullable=False, )
    status: Mapped[EmailSendJobStatus] = mapped_column( Enum(EmailSendJobStatus), default=EmailSendJobStatus.PENDING, nullable=False, index=True, )
    queue_name: Mapped[str] = mapped_column( String(100), default="emails", nullable=False, )

    celery_task_id: Mapped[str | None] = mapped_column( String(255), index=True, )
    attempts: Mapped[int] = mapped_column( Integer, default=0, nullable=False, )
    max_attempts: Mapped[int] = mapped_column( Integer, default=3, nullable=False, )

    started_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), )
    completed_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), )
    failed_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), )

    error_message: Mapped[str | None] = mapped_column( String(4000), )
    options: Mapped[dict | None] = mapped_column( JSON, )