from uuid import uuid4
from sqlalchemy import Column, String, Boolean, Index

from app.core.database import Base

from app.shared.mixins.audit_mixin import AuditMixin
from sqlalchemy.dialects.postgresql import UUID

class BaseModel(
    Base,
    AuditMixin,
):

    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )


