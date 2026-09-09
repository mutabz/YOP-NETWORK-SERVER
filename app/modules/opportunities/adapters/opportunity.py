from app.modules.opportunities.models.opportunity import (
    Opportunity,
)
from app.modules.opportunities.scraper.core.models import (
    MappedOpportunity,
)
from app.modules.opportunities.search import (
    SearchTermsBuilder,
)
from app.modules.opportunities.utils.slug import (
    slugify,
)


class OpportunityAdapter:
    """
    Converts a MappedOpportunity into the Opportunity
    domain model.

    Responsibilities:
        - generate the canonical opportunity slug
        - build the search alias index
        - transfer normalized mapped fields
        - create an Opportunity domain instance

    It does not:
        - persist to the database
        - perform deduplication
        - determine opportunity semantics
        - fetch or parse external content
    """

    def __init__(
        self,
        *,
        search_terms_builder: SearchTermsBuilder | None = None,
    ) -> None:
        self.search_terms_builder = (
            search_terms_builder
            or SearchTermsBuilder()
        )

    def to_model(
        self,
        mapped: MappedOpportunity,
        *,
        slug: str | None = None,
    ) -> Opportunity:
        """
        Convert a mapped scraper opportunity into
        an Opportunity domain model.

        Args:
            mapped:
                Normalized opportunity produced by a mapper.

            slug:
                Optional canonical slug override.

        Returns:
            Opportunity domain model instance.
        """

        canonical_slug = slug or slugify(
            mapped.title,
        )

        if not canonical_slug:
            raise ValueError(
                "Cannot create an opportunity without a valid slug."
            )

        slug_list = self.search_terms_builder.build(
            mapped,
        )

        return Opportunity(
            title=mapped.title,
            slug=canonical_slug,
            slug_list=slug_list,

            # Classification
            type=mapped.type,
            category=mapped.category,

            # Organization
            organization=mapped.organization,

            # Location
            country=mapped.country,
            city=mapped.city,
            location=mapped.location,
            remote=mapped.remote,

            # Dates
            deadline=mapped.deadline,
            start_date=mapped.start_date,
            end_date=mapped.end_date,
            published_at=mapped.published_at,

            # Content
            summary=mapped.summary,
            description=mapped.description,
            eligibility=mapped.eligibility,
            requirements=mapped.requirements,

            # Application
            application_url=mapped.application_url,

            # Source
            source_url=mapped.source_url,
            source_name=mapped.source_name,

            # Source-specific data
            extras=mapped.extras,
        )
