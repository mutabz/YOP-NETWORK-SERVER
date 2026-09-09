from datetime import datetime
from typing import Any
import re

from app.modules.opportunities.enums import OpportunityType
from app.modules.opportunities.scraper.core.bases import (
    BaseMapper,
)
from app.modules.opportunities.scraper.core.models import (
    MappedOpportunity,
    RawOpportunity,
)


class ScholarshipsAdsMapper(BaseMapper):
    """
    Maps ScholarshipsAds raw data into the normalized
    MappedOpportunity representation.

    The mapper only transforms data already extracted by
    ScholarshipsAdsParser.

    It does not:
        - fetch pages
        - parse HTML
        - discover URLs
        - invent source data
    """

    name = "scholarships_ads"

    def map(
        self,
        raw: RawOpportunity,
    ) -> MappedOpportunity:
        return MappedOpportunity(
            title=self._map_title(raw),
            type=self._map_type(raw),
            category=self._map_category(raw),
            organization=self._map_organization(raw),
            location=self._map_location(raw),
            country=self._map_country(raw),
            city=self._map_city(raw),
            remote=self._map_remote(raw),
            deadline=self._map_deadline(raw),
            start_date=self._map_start_date(raw),
            end_date=self._map_end_date(raw),
            published_at=self._map_published_at(raw),
            summary=self._map_summary(raw),
            description=self._map_description(raw),
            eligibility=self._map_eligibility(raw),
            requirements=self._map_requirements(raw),
            application_url=self._map_application_url(raw),
            source_url=raw.source_url,
            source_name=raw.source_name,
            extras=self._map_extras(raw),
        )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    @staticmethod
    def _map_title(
        raw: RawOpportunity,
    ) -> str:
        return (
            raw.title.strip()
            if raw.title
            else "Untitled Opportunity"
        )

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    @staticmethod
    def _map_type(
        raw: RawOpportunity,
    ) -> OpportunityType:
        return OpportunityType.SCHOLARSHIP

    @staticmethod
    def _map_category(
        raw: RawOpportunity,
    ) -> str | None:
        values = raw.extras.get(
            "degree_level",
            [],
        )

        text = ScholarshipsAdsMapper._join_values(
            values
        ).lower()

        if "phd" in text or "doctoral" in text:
            return "phd"

        if "master" in text:
            return "masters"

        if (
            "bachelor" in text
            or "undergraduate" in text
        ):
            return "undergraduate"

        if "postgraduate" in text:
            return "postgraduate"

        return None

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    @staticmethod
    def _map_organization(
        raw: RawOpportunity,
    ) -> str | None:
        return ScholarshipsAdsMapper._clean_value(
            raw.organization
        )

    # ------------------------------------------------------------------
    # Location
    # ------------------------------------------------------------------

    @staticmethod
    def _map_location(
        raw: RawOpportunity,
    ) -> str | None:
        return ScholarshipsAdsMapper._clean_value(
            raw.location
        )

    @staticmethod
    def _map_country(
        raw: RawOpportunity,
    ) -> str | None:
        return ScholarshipsAdsMapper._clean_value(
            raw.country
        )

    @staticmethod
    def _map_city(
        raw: RawOpportunity,
    ) -> str | None:
        return ScholarshipsAdsMapper._clean_value(
            raw.city
        )

    @staticmethod
    def _map_remote(
        raw: RawOpportunity,
    ) -> bool:
        return bool(raw.remote)

    # ------------------------------------------------------------------
    # Dates
    # ------------------------------------------------------------------

    @staticmethod
    def _map_deadline(
        raw: RawOpportunity,
    ) -> datetime | None:
        return ScholarshipsAdsMapper._parse_datetime(
            raw.deadline
        )

    @staticmethod
    def _map_start_date(
        raw: RawOpportunity,
    ) -> datetime | None:
        return ScholarshipsAdsMapper._parse_datetime(
            raw.start_date
        )

    @staticmethod
    def _map_end_date(
        raw: RawOpportunity,
    ) -> datetime | None:
        return ScholarshipsAdsMapper._parse_datetime(
            raw.end_date
        )

    @staticmethod
    def _map_published_at(
        raw: RawOpportunity,
    ) -> datetime | None:
        """
        Map the published date extracted by the parser.

        The parser stores it directly on RawOpportunity,
        for example:

            "04 Sep 2026"

        The mapper converts it into datetime.
        """

        return ScholarshipsAdsMapper._parse_datetime(
            raw.published_at
        )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    @staticmethod
    def _map_summary(
        raw: RawOpportunity,
    ) -> list[str] | None:
        """
        Use the first two paragraphs of the description
        as the normalized summary.
        """

        paragraphs = (
            ScholarshipsAdsMapper._map_description(
                raw
            )
        )

        if not paragraphs:
            return None

        return paragraphs[:2]

    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------

    @staticmethod
    def _map_description(
        raw: RawOpportunity,
    ) -> list[str] | None:
        """
        Convert the parser's raw description into
        normalized paragraphs.
        """

        if not raw.description:
            return None

        paragraphs = [
            paragraph.strip()
            for paragraph in raw.description.split(
                "\n\n"
            )
            if paragraph.strip()
        ]

        return paragraphs or None

    # ------------------------------------------------------------------
    # Eligibility
    # ------------------------------------------------------------------

    @staticmethod
    def _map_eligibility(
        raw: RawOpportunity,
    ) -> list[str] | None:
        """
        Map the source's explicit eligibility criteria
        into the canonical eligibility field.
        """

        values = raw.extras.get(
            "eligibility_criteria"
        )

        return ScholarshipsAdsMapper._normalize_strings(
            values
        )

    # ------------------------------------------------------------------
    # Requirements
    # ------------------------------------------------------------------

    @staticmethod
    def _map_requirements(
        raw: RawOpportunity,
    ) -> list[str] | None:
        """
        Map an explicit requirements section.

        We deliberately do not convert eligibility criteria
        into requirements because those are different concepts.
        """

        values = raw.extras.get(
            "requirements"
        )

        return ScholarshipsAdsMapper._normalize_strings(
            values
        )

    # ------------------------------------------------------------------
    # Application URL
    # ------------------------------------------------------------------

    @staticmethod
    def _map_application_url(
        raw: RawOpportunity,
    ) -> str | None:
        """
        Use the application URL extracted directly by
        the parser.

        If ScholarshipsAds uses href="#", the parser returns
        None and no fake application URL is created.
        """

        return ScholarshipsAdsMapper._clean_value(
            raw.application_url
        )

    # ------------------------------------------------------------------
    # Extras
    # ------------------------------------------------------------------

    @staticmethod
    def _map_extras(
        raw: RawOpportunity,
    ) -> dict[str, Any]:
        """
        Preserve source-specific information that does not
        belong to the canonical MappedOpportunity fields.

        Canonical fields are intentionally removed from extras
        to avoid duplicating the normalized representation.
        """

        extras = dict(raw.extras)

        # These are canonical fields and already have their own
        # fields in MappedOpportunity.
        canonical_keys = {
            "published_at",
            "application_url",
            "requirements",
            "eligibility",
        }

        for key in canonical_keys:
            extras.pop(key, None)

        return extras

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_strings(
        values: Any,
    ) -> list[str] | None:
        """
        Normalize extracted values into list[str].
        """

        if not values:
            return None

        if isinstance(values, str):
            value = value.strip()

            return [value] if value else None

        if not isinstance(values, list):
            return None

        result: list[str] = []

        for value in values:
            if isinstance(value, str):
                value = value.strip()

                if value:
                    result.append(value)

        return result or None

    @staticmethod
    def _join_values(
        values: Any,
    ) -> str:
        """
        Convert extracted values into searchable text.
        """

        if isinstance(values, str):
            return values

        if isinstance(values, list):
            return " ".join(
                value
                for value in values
                if isinstance(value, str)
            )

        return str(values)

    @staticmethod
    def _clean_value(
        value: str | None,
    ) -> str | None:
        if not value:
            return None

        value = value.strip()

        return value or None

    @staticmethod
    def _parse_datetime(
        value: str | None,
    ) -> datetime | None:
        """
        Parse common date formats returned by
        ScholarshipsAds.

        Supported examples:

            2026-09-30
            2026-09-30T12:30:00
            04 Sep 2026
            Deadline: 31 Jan 2027
            Published on: 04 Sep 2026
        """

        if not value:
            return None

        value = value.strip()

        # Remove common ScholarshipsAds labels.
        value = re.sub(
            r"^(deadline|published\s+on|published)\s*:\s*",
            "",
            value,
            flags=re.IGNORECASE,
        )

        value = value.strip()

        if not value:
            return None

        # ISO formats
        try:
            return datetime.fromisoformat(
                value.replace(
                    "Z",
                    "+00:00",
                )
            )
        except ValueError:
            pass

        # ScholarshipsAds date formats
        for fmt in (
            "%d %b %Y",
            "%d %B %Y",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
        ):
            try:
                return datetime.strptime(
                    value,
                    fmt,
                )
            except ValueError:
                continue

        return None
