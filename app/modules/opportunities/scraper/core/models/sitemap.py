from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class SitemapEntry:
    """
    A URL discovered from a sitemap.
    """

    url: str

    last_modified: datetime | None = None

    change_frequency: str | None = None

    priority: float | None = None


@dataclass(slots=True, frozen=True)
class SitemapIndexEntry:
    """
    A sitemap URL discovered from a sitemap index.
    """

    url: str

    last_modified: datetime | None = None