from __future__ import annotations

import uuid

from sqlalchemy import (
    Boolean, Enum, Integer,
    JSON, String, Text,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_model import BaseModelSys

from app.integrations.email.enums import (
    EmailType,
    EmailSourceModule,
)


class EmailTemplateVersion(BaseModelSys):

    __tablename__ = "system_email_template_versions"


    template_id: Mapped[uuid.UUID] = mapped_column( UUID(as_uuid=True), ForeignKey( "system_email_templates.id", ondelete="CASCADE", ), nullable=False, index=True, )
    version: Mapped[int] = mapped_column( Integer, nullable=False, )
    source_module: Mapped[EmailSourceModule] = mapped_column( Enum(EmailSourceModule), nullable=False, )
    email_type: Mapped[EmailType] = mapped_column( Enum(EmailType), nullable=False, )

    subject_template: Mapped[str] = mapped_column( String(500), nullable=False, )
    html_template: Mapped[str] = mapped_column( Text, nullable=False, )
    text_template: Mapped[str | None] = mapped_column( Text, )
    variables: Mapped[dict | None] = mapped_column( JSON, )

    checksum: Mapped[str | None] = mapped_column( String(255), unique=True, )
    changelog: Mapped[str | None] = mapped_column( Text, )

    published: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False, )