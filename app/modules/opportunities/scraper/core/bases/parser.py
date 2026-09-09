from abc import ABC, abstractmethod

from app.modules.opportunities.scraper.core.models import (
    RawOpportunity,
)


class BaseParser(ABC):
    """
    Base contract for source-specific parsers.

    A parser converts raw source content, usually HTML,
    into a RawOpportunity.
    """

    name: str

    def __init__(
        self,
        *,
        config: dict | None = None,
    ) -> None:
        self.config = config or {}

    @abstractmethod
    def parse(
        self,
        html: str,
        *,
        source_url: str,
    ) -> RawOpportunity:
        """
        Parse a single opportunity page.

        Args:
            html: Raw HTML content.
            source_url: URL of the page being parsed.

        Returns:
            RawOpportunity containing extracted source data.
        """
        raise NotImplementedError