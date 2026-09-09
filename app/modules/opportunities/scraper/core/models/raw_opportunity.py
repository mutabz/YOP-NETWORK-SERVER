# app/modules/opportunities/scraper/models/raw_opportunity.py

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RawOpportunity:
    """
    Raw data extracted from an opportunity source.

    This represents what the scraper found, not yet the final
    application/domain representation.
    """

    source_name: str
    source_url: str

    # Raw identity
    title: str | None = None
    url: str | None = None

    # Application
    application_url: str | None = None

    # Raw content
    description: str | None = None


    summary: str | None = None

    # Raw organization/location
    organization: str | None = None
    location: str | None = None
    country: str | None = None
    city: str | None = None

    # Raw classification
    type: str | None = None
    category: str | None = None

    # Raw dates
    deadline: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    published_at: str | None = None

    # Raw metadata
    remote: bool | None = None

    # Anything source-specific
    extras: dict[str, Any] = field(default_factory=dict)