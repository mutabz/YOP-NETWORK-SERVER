from dataclasses import dataclass

from app.modules.opportunities.scraper.core.models import (
    MappedOpportunity,
)
from app.modules.opportunities.utils.slug import (
    slugify,
)


@dataclass(frozen=True, slots=True)
class OpportunityIdentity:
    """
    Stable identity information used to identify an opportunity.

    This class does not query the database and does not perform
    persistence.

    It only derives deterministic identity candidates from a
    mapped opportunity.
    """

    slug: str
    source_url: str
    source_name: str | None = None

    @classmethod
    def from_mapped(
        cls,
        mapped: MappedOpportunity,
    ) -> "OpportunityIdentity":
        """
        Build identity information from a mapped opportunity.
        """

        slug = slugify(mapped.title)

        if not slug:
            raise ValueError(
                "Cannot create opportunity identity "
                "without a valid title."
            )

        if not mapped.source_url:
            raise ValueError(
                "Cannot create opportunity identity "
                "without a source URL."
            )

        return cls(
            slug=slug,
            source_url=mapped.source_url,
            source_name=mapped.source_name,
        )
