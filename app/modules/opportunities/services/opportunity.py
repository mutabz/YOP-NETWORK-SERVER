from datetime import datetime, timezone

from app.shared.base_service import BaseService

from app.modules.opportunities.enums import OpportunityStatus

from app.modules.opportunities.repositories import (
    OpportunityRepository,
)

from app.modules.opportunities.schemas import (
    OpportunityCreate,
    OpportunityUpdate,
)

from app.modules.opportunities.adapters import (
    OpportunityAdapter,
)

from app.modules.opportunities.scraper.core.models import (
    MappedOpportunity,
)

from app.modules.opportunities.utils.slug import (
    slugify,
)


class OpportunityService(BaseService):

    model_name = "opportunities"

    create_schema = OpportunityCreate
    update_schema = OpportunityUpdate

    def __init__(
        self,
        repository: OpportunityRepository,
        adapter: OpportunityAdapter | None = None,
    ):
        super().__init__(repository)

        self.adapter = (
            adapter
            or OpportunityAdapter()
        )

    # =========================================================
    # UPDATE
    # =========================================================

    async def before_update(
        self,
        opportunity_id,
        data: dict,
    ):
        """
        Validate and normalize opportunity updates.
        """

        opportunity = await self.repository.get(
            opportunity_id
        )

        if not opportunity:
            raise ValueError(
                "Opportunity not found"
            )

        # -----------------------------------------------------
        # Normalize strings
        # -----------------------------------------------------

        title = data.get("title")
        slug = data.get("slug")
        source_url = data.get("source_url")
        source_name = data.get("source_name")
        organization = data.get("organization")

        if title:
            data["title"] = title.strip()

        if slug:
            data["slug"] = slug.strip().lower()

        if source_url:
            data["source_url"] = source_url.strip()

        if source_name:
            data["source_name"] = source_name.strip()

        if organization:
            data["organization"] = organization.strip()

        # -----------------------------------------------------
        # Slug uniqueness
        # -----------------------------------------------------

        if (
            slug
            and data["slug"] != opportunity.slug
        ):
            existing = await self.repository.find_by_slug(
                data["slug"]
            )

            if (
                existing
                and existing.id != opportunity.id
            ):
                raise ValueError(
                    "Opportunity with this slug already exists"
                )

        # -----------------------------------------------------
        # Source URL uniqueness
        # -----------------------------------------------------

        if (
            source_url
            and data["source_url"] != opportunity.source_url
        ):
            existing = (
                await self.repository.find_by_source_url(
                    data["source_url"]
                )
            )

            if (
                existing
                and existing.id != opportunity.id
            ):
                raise ValueError(
                    "Opportunity with this source URL already exists"
                )

        return data

    # =========================================================
    # INGEST
    # =========================================================

    async def ingest(
        self,
        mapped: MappedOpportunity,
    ):
        """
        Ingest an opportunity discovered by a scraper.

        Identity priority:

            1. Exact source URL
            2. Source + canonical slug
            3. Global canonical slug
            4. Create new opportunity

        Existing records are updated.

        New records are created as DRAFT.

        Scraper ingestion never automatically changes an
        existing publishing status.
        """

        # -----------------------------------------------------
        # Build domain model
        # -----------------------------------------------------

        opportunity = self.adapter.to_model(
            mapped
        )

        # -----------------------------------------------------
        # 1. Exact source URL
        # -----------------------------------------------------

        existing = await self.repository.find_by_source_url(
            opportunity.source_url
        )

        if existing:
            return await self._update_from_ingestion(
                existing,
                opportunity,
            )

        # -----------------------------------------------------
        # 2. Source + slug
        # -----------------------------------------------------

        if opportunity.source_name:

            existing = (
                await self.repository.find_by_source_and_slug(
                    source_name=opportunity.source_name,
                    slug=opportunity.slug,
                )
            )

            if existing:
                return await self._update_from_ingestion(
                    existing,
                    opportunity,
                )

        # -----------------------------------------------------
        # 3. Global slug
        # -----------------------------------------------------

        existing = await self.repository.find_by_slug(
            opportunity.slug
        )

        if existing:

            # -------------------------------------------------
            # Same source
            # -------------------------------------------------

            if (
                existing.source_name
                == opportunity.source_name
            ):
                return await self._update_from_ingestion(
                    existing,
                    opportunity,
                )

            # -------------------------------------------------
            # Different source
            #
            # Same title does not necessarily mean the same
            # opportunity.
            #
            # Generate a source-scoped slug.
            # -------------------------------------------------

            opportunity.slug = (
                self._build_source_slug(
                    opportunity.slug,
                    opportunity.source_name,
                )
            )

            # -------------------------------------------------
            # Check the generated slug too.
            # -------------------------------------------------

            existing = await self.repository.find_by_slug(
                opportunity.slug
            )

            if existing:

                # If this points to the same source URL,
                # update rather than create.
                if (
                    existing.source_url
                    == opportunity.source_url
                ):
                    return await self._update_from_ingestion(
                        existing,
                        opportunity,
                    )

                # Extremely unlikely deterministic collision.
                opportunity.slug = (
                    self._build_collision_slug(
                        opportunity.slug,
                        opportunity.source_url,
                    )
                )

        # -----------------------------------------------------
        # 4. Create
        # -----------------------------------------------------

        return await self._create_from_ingestion(
            opportunity
        )

    # =========================================================
    # CREATE FROM INGESTION
    # =========================================================

    async def _create_from_ingestion(
        self,
        opportunity,
    ):
        """
        Create a newly discovered scraped opportunity.

        Scraped opportunities start as DRAFT.
        """

        return await self.repository.create(
            title=opportunity.title,
            slug=opportunity.slug,
            slug_list=opportunity.slug_list,

            # Classification
            type=opportunity.type,
            category=opportunity.category,

            # Organization
            organization=opportunity.organization,

            # Location
            country=opportunity.country,
            city=opportunity.city,
            location=opportunity.location,
            remote=opportunity.remote,

            # Dates
            deadline=opportunity.deadline,
            start_date=opportunity.start_date,
            end_date=opportunity.end_date,
            published_at=opportunity.published_at,

            # Content
            summary=opportunity.summary,
            description=opportunity.description,
            eligibility=opportunity.eligibility,
            requirements=opportunity.requirements,

            # Application
            application_url=opportunity.application_url,

            # Source
            source_url=opportunity.source_url,
            source_name=opportunity.source_name,

            # Publishing
            status=OpportunityStatus.DRAFT,

            # Source-specific data
            extras=opportunity.extras,
        )

    # =========================================================
    # UPDATE FROM INGESTION
    # =========================================================

    async def _update_from_ingestion(
        self,
        existing,
        incoming,
    ):
        """
        Update an existing opportunity using fresh scraper data.

        The existing publishing status is intentionally preserved.
        """

        data = {
            "title": incoming.title,
            "slug": existing.slug,
            "slug_list": incoming.slug_list,

            # Classification
            "type": incoming.type,
            "category": incoming.category,

            # Organization
            "organization": incoming.organization,

            # Location
            "country": incoming.country,
            "city": incoming.city,
            "location": incoming.location,
            "remote": incoming.remote,

            # Dates
            "deadline": incoming.deadline,
            "start_date": incoming.start_date,
            "end_date": incoming.end_date,
            "published_at": incoming.published_at,

            # Content
            "summary": incoming.summary,
            "description": incoming.description,
            "eligibility": incoming.eligibility,
            "requirements": incoming.requirements,

            # Application
            "application_url": incoming.application_url,

            # Source
            "source_url": incoming.source_url,
            "source_name": incoming.source_name,

            # Source-specific data
            "extras": incoming.extras,
        }

        return await self.repository.update(
            existing.id,
            **data,
        )

    # =========================================================
    # SOURCE SLUG
    # =========================================================

    @staticmethod
    def _build_source_slug(
        slug: str,
        source_name: str | None,
    ) -> str:
        """
        Build a deterministic source-scoped slug.

        Example:

            global-scholarship-2027
            +
            scholarships_ads

            →

            global-scholarship-2027-scholarships-ads
        """

        if not source_name:
            return slug

        source_slug = slugify(
            source_name
        )

        if not source_slug:
            return slug

        return f"{slug}-{source_slug}"

    # =========================================================
    # COLLISION SLUG
    # =========================================================

    @staticmethod
    def _build_collision_slug(
        slug: str,
        source_url: str,
    ) -> str:
        """
        Generate a deterministic fallback slug when an
        extremely unlikely source-scoped slug collision occurs.

        The URL hash keeps the slug deterministic without
        exposing the entire source URL in the slug.
        """

        import hashlib

        digest = hashlib.sha256(
            source_url.encode("utf-8")
        ).hexdigest()[:10]

        return f"{slug}-{digest}"

    # =========================================================
    # PUBLISH
    # =========================================================

    async def publish(
        self,
        opportunity_id: str,
    ):

        opportunity = await self.repository.get(
            opportunity_id
        )

        if not opportunity:
            raise ValueError(
                "Opportunity not found"
            )

        if (
            opportunity.status
            == OpportunityStatus.ARCHIVED
        ):
            raise ValueError(
                "Archived opportunities cannot be published"
            )

        if (
            opportunity.status
            == OpportunityStatus.PUBLISHED
        ):
            return opportunity

        return await self.repository.update(
            opportunity.id,
            status=OpportunityStatus.PUBLISHED,
            published_at=datetime.now(
                timezone.utc
            ),
        )

    # =========================================================
    # CLOSE
    # =========================================================

    async def close(
        self,
        opportunity_id: str,
    ):

        opportunity = await self.repository.get(
            opportunity_id
        )

        if not opportunity:
            raise ValueError(
                "Opportunity not found"
            )

        if (
            opportunity.status
            != OpportunityStatus.PUBLISHED
        ):
            raise ValueError(
                "Only published opportunities can be closed"
            )

        return await self.repository.update(
            opportunity.id,
            status=OpportunityStatus.CLOSED,
        )

    # =========================================================
    # EXPIRE
    # =========================================================

    async def expire(
        self,
        opportunity_id: str,
    ):

        opportunity = await self.repository.get(
            opportunity_id
        )

        if not opportunity:
            raise ValueError(
                "Opportunity not found"
            )

        if (
            opportunity.status
            != OpportunityStatus.PUBLISHED
        ):
            raise ValueError(
                "Only published opportunities can be expired"
            )

        return await self.repository.update(
            opportunity.id,
            status=OpportunityStatus.EXPIRED,
        )

    # =========================================================
    # ARCHIVE
    # =========================================================

    async def archive(
        self,
        opportunity_id: str,
    ):

        opportunity = await self.repository.get(
            opportunity_id
        )

        if not opportunity:
            raise ValueError(
                "Opportunity not found"
            )

        if (
            opportunity.status
            == OpportunityStatus.ARCHIVED
        ):
            return opportunity

        return await self.repository.update(
            opportunity.id,
            status=OpportunityStatus.ARCHIVED,
        )

