from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class AuditMixin:

    created_at = Column( DateTime, default=datetime.utcnow, nullable=True )
    updated_at = Column( DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True )

