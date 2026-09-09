import re
import unicodedata
from collections.abc import Iterable
from typing import Any

from app.modules.opportunities.enums import OpportunityType
from app.modules.opportunities.scraper.core.models import (
    MappedOpportunity,
)

from .aliases import (
    CATEGORY_ALIASES,
    COUNTRY_ALIASES,
    DEGREE_ALIASES,
    REMOTE_ALIASES,
    TYPE_ALIASES,
)

SEARCH_STOP_WORDS: frozenset[str] = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "by",
        "for",
        "from",
        "in",
        "into",
        "is",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    }
)

class SearchTermsBuilder:
    """
    Builds searchable aliases for an opportunity.

    `slug_list` is a search index, not a collection of
    historical URL slugs.

    The builder combines:
        - title
        - opportunity type
        - category
        - degree/study level
        - organization
        - country
        - city
        - location
        - remote status
        - source-specific extras

    The result contains normalized, deduplicated search terms.
    """

    def build(
        self,
        opportunity: MappedOpportunity,
    ) -> list[str]:
        terms: set[str] = set()

        # --------------------------------------------------------------
        # Title
        # --------------------------------------------------------------

        self._add_text(
            terms,
            opportunity.title,
        )

        # --------------------------------------------------------------
        # Type
        # --------------------------------------------------------------

        self._add_aliases(
            terms,
            TYPE_ALIASES.get(
                opportunity.type,
                (),
            ),
        )

        # --------------------------------------------------------------
        # Category
        # --------------------------------------------------------------

        if opportunity.category:
            self._add_text(
                terms,
                opportunity.category,
            )

            self._add_aliases(
                terms,
                CATEGORY_ALIASES.get(
                    opportunity.category.lower(),
                    (),
                ),
            )

        # --------------------------------------------------------------
        # Organization
        # --------------------------------------------------------------

        self._add_text(
            terms,
            opportunity.organization,
        )

        # --------------------------------------------------------------
        # Country
        # --------------------------------------------------------------

        if opportunity.country:
            self._add_text(
                terms,
                opportunity.country,
            )

            country_key = (
                self._normalize_lookup_key(
                    opportunity.country,
                )
            )

            self._add_aliases(
                terms,
                COUNTRY_ALIASES.get(
                    country_key,
                    (),
                ),
            )

        # --------------------------------------------------------------
        # City
        # --------------------------------------------------------------

        self._add_text(
            terms,
            opportunity.city,
        )

        # --------------------------------------------------------------
        # Location
        # --------------------------------------------------------------

        self._add_text(
            terms,
            opportunity.location,
        )

        # --------------------------------------------------------------
        # Remote
        # --------------------------------------------------------------

        if opportunity.remote:
            self._add_aliases(
                terms,
                REMOTE_ALIASES,
            )

        # --------------------------------------------------------------
        # Source-specific data
        # --------------------------------------------------------------

        self._extract_extras(
            terms,
            opportunity.extras,
        )

        return sorted(terms)

    def _add_degree_terms(
        self,
        terms: set[str],
        value: str,
    ) -> None:
        normalized = self._normalize_text(value)

        # Keep the original degree value searchable.
        self._add_text(
            terms,
            value,
        )

        # Undergraduate / Bachelor's
        if any(
            token in normalized
            for token in (
                "bachelor",
                "undergraduate",
            )
        ):
            self._add_aliases(
                terms,
                DEGREE_ALIASES["undergraduate"],
            )

        # Master's
        if any(
            token in normalized
            for token in (
                "master",
                "masters",
            )
        ):
            self._add_aliases(
                terms,
                DEGREE_ALIASES["masters"],
            )

        # PhD / Doctoral
        if any(
            token in normalized
            for token in (
                "phd",
                "doctoral",
                "doctorate",
            )
        ):
            self._add_aliases(
                terms,
                DEGREE_ALIASES["phd"],
            )

        # Postgraduate
        if "postgraduate" in normalized:
            self._add_aliases(
                terms,
                DEGREE_ALIASES["postgraduate"],
            )


    # ------------------------------------------------------------------
    # Extras
    # ------------------------------------------------------------------

    def _extract_extras(
        self,
        terms: set[str],
        extras: dict[str, Any],
    ) -> None:
        for key, value in extras.items():
            # Technical metadata should not become search terms.
            if key in {
                "published_at",
            }:
                continue

            # ScholarshipsAds degree information needs semantic
            # expansion because it may contain multiple levels.
            if key == "card" and isinstance(value, dict):
                degree = value.get("degree")

                if isinstance(degree, str):
                    self._add_degree_terms(
                        terms,
                        degree,
                    )

                # The rest of the card metadata is still searchable.
                for card_key, card_value in value.items():
                    if card_key == "degree":
                        continue

                    self._add_text(
                        terms,
                        card_key,
                    )

                    self._extract_value(
                        terms,
                        card_value,
                    )

                continue

            self._extract_value(
                terms,
                value,
            )

    def _extract_value(
        self,
        terms: set[str],
        value: Any,
    ) -> None:

        if value is None:
            return

        if isinstance(value, str):
            self._add_text(
                terms,
                value,
            )
            return

        if isinstance(value, (list, tuple, set)):
            for item in value:
                self._extract_value(
                    terms,
                    item,
                )
            return

        if isinstance(value, dict):
            for key, item in value.items():

                self._add_text(
                    terms,
                    key,
                )

                self._extract_value(
                    terms,
                    item,
                )

    # ------------------------------------------------------------------
    # Text handling
    # ------------------------------------------------------------------

    def _add_text(
        self,
        terms: set[str],
        value: str | None,
    ) -> None:
        if not value:
            return

        normalized = self._normalize_text(
            value,
        )

        if not normalized:
            return

        # Full phrase.
        terms.add(normalized)

        # Individual meaningful words.
        for word in normalized.split("-"):
            if self._is_meaningful_word(word):
                terms.add(word)

    def _add_aliases(
        self,
        terms: set[str],
        aliases: Iterable[str],
    ) -> None:
        for alias in aliases:
            normalized = self._normalize_text(
                alias,
            )

            if normalized:
                terms.add(normalized)

    # ------------------------------------------------------------------
    # Normalization
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_text(
        value: str,
    ) -> str:
        value = unicodedata.normalize(
            "NFKD",
            value,
        )

        value = value.encode(
            "ascii",
            "ignore",
        ).decode("ascii")

        value = value.lower().strip()

        value = re.sub(
            r"['’`]",
            "",
            value,
        )

        value = re.sub(
            r"[^a-z0-9]+",
            "-",
            value,
        )

        value = re.sub(
            r"-+",
            "-",
            value,
        )

        return value.strip("-")

    @staticmethod
    def _normalize_lookup_key(
        value: str,
    ) -> str:
        return (
            value.lower()
            .strip()
        )

    @staticmethod
    def _is_meaningful_word(
        value: str,
    ) -> bool:
        if not value:
            return False

        if value in SEARCH_STOP_WORDS:
            return False

        return len(value) >= 2