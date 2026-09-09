from app.shared.base_model import BaseModel

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SAEnum,
    JSON,
    String,
    Text,
    func,
)
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column
from app.modules.opportunities.enums import (
    OpportunityStatus,
    OpportunityType
)

class Opportunity(BaseModel):
    __tablename__ = "opportunities"

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    slug: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
        index=True
    )
    slug_list: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    # Classification
    type: Mapped[OpportunityType] = mapped_column(
        SAEnum(
            OpportunityType,
            name="opportunity_type"
        ),
        nullable=False,
        index=True
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    # Organization
    organization: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    # Location
    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    remote: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # Dates
    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True
    )

    start_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Content
    summary: Mapped[list[Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    description: Mapped[list[Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    eligibility: Mapped[list[Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    requirements: Mapped[list[Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    application_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # Source
    source_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    source_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    # Publishing
    status: Mapped[OpportunityStatus] = mapped_column(
        SAEnum(
            OpportunityStatus,
            name="opportunity_status"
        ),
        default=OpportunityStatus.DRAFT,
        nullable=False,
        index=True
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Flexible source-specific data
    extras: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False
    )
