from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.modules.opportunities.enums import OpportunityType


@dataclass(slots=True)
class MappedOpportunity:
    """
    Source-independent representation of an opportunity.

    This is the normalized structural shape produced by a
    source mapper before the final Opportunity domain model
    is created.
    """

    # Identity
    title: str

    # Classification
    type: OpportunityType
    category: str | None = None

    # Organization
    organization: str | None = None

    # Location
    country: str | None = None
    city: str | None = None
    location: str | None = None
    remote: bool = False

    # Dates
    deadline: datetime | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    published_at: datetime | None = None

    # Content
    summary: list[Any] | None = None
    description: list[Any] | None = None
    eligibility: list[Any] | None = None
    requirements: list[Any] | None = None

    # URLs
    application_url: str | None = None
    source_url: str | None = None
    source_name: str | None = None

    # Flexible source-specific data
    extras: dict[str, Any] = field(default_factory=dict)