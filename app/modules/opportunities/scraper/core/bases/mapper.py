from abc import ABC, abstractmethod

from app.modules.opportunities.scraper.core.models import (
    MappedOpportunity,
    RawOpportunity,
)


class BaseMapper(ABC):
    """
    Base contract for converting raw source data into the
    source-independent opportunity representation.
    """

    name: str

    def __init__(
        self,
        *,
        config: dict | None = None,
    ) -> None:
        self.config = config or {}

    @abstractmethod
    def map(
        self,
        raw: RawOpportunity,
    ) -> MappedOpportunity:
        """
        Convert raw scraped data into a mapped opportunity.
        """
        raise NotImplementedError