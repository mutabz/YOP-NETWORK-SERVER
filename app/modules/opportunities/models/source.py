from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Enum as SAEnum, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_model import BaseModel
from app.modules.opportunities.enums import ( SourceType )


class OpportunitySource(BaseModel):
    __tablename__ = "opportunity_sources"

    # Identity
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    source_type: Mapped[SourceType] = mapped_column(
        SAEnum(
            SourceType,
            name="source_type",
        ),
        nullable=False,
    )

    # Scraper configuration
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    config: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    last_scraped_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    next_scrape_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )