from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.modules.opportunities.scraper.core.bases.fetcher import (
    BaseFetcher,
)
from app.modules.opportunities.scraper.core.models.raw_opportunity import (
    RawOpportunity,
)


class BaseSource(ABC):
    """
    Base contract for all opportunity sources.

    A source coordinates source-specific discovery and extraction,
    while delegating HTTP fetching and parsing to dedicated
    components.
    """

    name: str

    def __init__(
        self,
        *,
        source_url: str,
        fetcher: BaseFetcher,
        config: dict | None = None,
    ) -> None:
        self.source_url = source_url
        self.fetcher = fetcher
        self.config = config or {}

    @abstractmethod
    async def scrape(self) -> AsyncIterator[RawOpportunity]:
        """
        Extract opportunities from the source.

        Yields:
            RawOpportunity objects.
        """
        raise NotImplementedError