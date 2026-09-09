from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, Enum, Integer,
    JSON, String, Text,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_model import BaseModelSys

from app.integrations.email.enums import (
    EmailSourceModule,
    EmailType, EmailTemplateCode
)


class EmailTemplate(BaseModelSys):

    __tablename__ = "system_email_templates"


    tenant_id: Mapped[uuid.UUID] = mapped_column( UUID(as_uuid=True), nullable=False, index=True, )
    company_id: Mapped[uuid.UUID] = mapped_column( UUID(as_uuid=True), nullable=False, index=True, )

    name: Mapped[str] = mapped_column( String(150), nullable=False, )
    code: Mapped[EmailTemplateCode] = mapped_column( String(100), nullable=False, unique=True, index=True, )
    description: Mapped[str | None] = mapped_column( String(1000), )
    source_module: Mapped[EmailSourceModule] = mapped_column( Enum(EmailSourceModule), nullable=False, index=True, )
    email_type: Mapped[EmailType] = mapped_column( Enum(EmailType), nullable=False, index=True, )

    version: Mapped[int] = mapped_column( Integer, default=1, nullable=False, )
    subject_template: Mapped[str] = mapped_column( String(500), nullable=False, )
    html_template: Mapped[str] = mapped_column( Text, nullable=False, )
    text_template: Mapped[str | None] = mapped_column( Text, )
    variables: Mapped[dict | None] = mapped_column( JSON, )

    author: Mapped[str | None] = mapped_column( String(150), )
    category: Mapped[str | None] = mapped_column( String(100), )
    tags: Mapped[dict | None] = mapped_column( JSON, )

    is_default: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False, )
    is_system: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False, )
    is_active: Mapped[bool] = mapped_column( Boolean, default=True, nullable=False, )
    is_public: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False, )
    published_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), )