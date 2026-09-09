from __future__ import annotations

import uuid

from sqlalchemy import (
    Boolean, ForeignKey,
    Integer, String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_model import BaseModelSys


class EmailAttachment(BaseModelSys):

    __tablename__ = "system_email_attachments"

    email_id: Mapped[uuid.UUID] = mapped_column( UUID(as_uuid=True), ForeignKey( "system_emails.id", ondelete="CASCADE", ), nullable=False, index=True, )
    document_id: Mapped[uuid.UUID | None] = mapped_column( UUID(as_uuid=True), ForeignKey( "system_documents.id", ondelete="SET NULL", ), index=True, )
    document_file_id: Mapped[uuid.UUID | None] = mapped_column( UUID(as_uuid=True), ForeignKey( "system_document_files.id", ondelete="SET NULL", ), index=True, )

    filename: Mapped[str] = mapped_column( String(255), nullable=False, )
    mime_type: Mapped[str] = mapped_column( String(150), nullable=False, )
    file_size: Mapped[int] = mapped_column( Integer, default=0, nullable=False, )
    is_inline: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False, )
    content_id: Mapped[str | None] = mapped_column( String(255), )