import re

from bs4 import BeautifulSoup, Tag

from app.modules.opportunities.scraper.core.bases import (
    BaseParser,
)
from app.modules.opportunities.scraper.core.models import (
    RawOpportunity,
)

from .selectors import ScholarshipsAdsSelectors


class ScholarshipsAdsParser(BaseParser):
    """
    Parser for individual ScholarshipsAds opportunity pages.

    Responsible only for extracting raw values from HTML.

    It does not:
        - normalize semantic values
        - convert dates
        - determine OpportunityType
        - map fields to the domain model
    """

    name = "scholarships_ads"

    def parse(
        self,
        html: str,
        *,
        source_url: str,
    ) -> RawOpportunity:
        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        title = self._text(
            soup,
            ScholarshipsAdsSelectors.TITLE,
        )

        sections = self._extract_sections(
            soup,
            title=title,
        )

        card_metadata = self._extract_card_metadata(
            soup,
        )

        application_url = self._extract_application_url(
            soup,
        )

        published_at = self._extract_published_date(
            soup,
        )

        extras = {
            **sections,
            "card": card_metadata,
        }

        if published_at:
            extras["published_at"] = published_at

        return RawOpportunity(
            source_name=self.name,
            source_url=source_url,
            title=title,
            url=source_url,
            application_url=application_url,
            description=self._extract_description(
                soup,
                title=title,
            ),
            organization=card_metadata.get(
                "organization",
            ),
            location=card_metadata.get(
                "country",
            ),
            country=card_metadata.get(
                "country",
            ),
            deadline=card_metadata.get(
                "deadline",
            ),
            published_at=published_at,
            extras=extras,
        )

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _extract_sections(
        self,
        soup: BeautifulSoup,
        *,
        title: str | None = None,
    ) -> dict[str, list[str]]:
        """
        Extract content grouped by h2/h3 headings.

        Section names are normalized into safe keys.

        Example:

            "Study at 3 Universities: Harvard, Oxford..."

        becomes:

            "study_at_3_universities_harvard_oxford..."
        """

        sections: dict[str, list[str]] = {}

        headings = soup.select(
            ScholarshipsAdsSelectors.SECTION_HEADINGS,
        )

        normalized_title = (
            self._normalize_section_name(title)
            if title
            else None
        )

        for heading in headings:
            heading_text = heading.get_text(
                " ",
                strip=True,
            )

            section_name = (
                self._normalize_section_name(
                    heading_text,
                )
            )

            if not section_name:
                continue

            # Do not store the page title if it appears
            # again as an article heading.
            if section_name == normalized_title:
                continue

            content = self._collect_section_content(
                heading,
            )

            if content:
                sections[section_name] = content

        return sections

    def _collect_section_content(
        self,
        heading: Tag,
    ) -> list[str]:
        """
        Collect paragraphs and list items until the next
        h2/h3 heading.
        """

        content: list[str] = []

        for sibling in heading.next_siblings:
            if not isinstance(sibling, Tag):
                continue

            if sibling.name in {"h2", "h3"}:
                break

            if sibling.name == "p":
                text = self._clean_text(
                    sibling.get_text(
                        " ",
                        strip=True,
                    )
                )

                if text:
                    content.append(text)

            elif sibling.name in {"ul", "ol"}:
                for item in sibling.select("li"):
                    text = self._clean_text(
                        item.get_text(
                            " ",
                            strip=True,
                        )
                    )

                    if text:
                        content.append(text)

            elif sibling.name in {
                "div",
                "blockquote",
            }:
                text = self._clean_text(
                    sibling.get_text(
                        " ",
                        strip=True,
                    )
                )

                if text:
                    content.append(text)

        return content

    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------

    def _extract_description(
        self,
        soup: BeautifulSoup,
        *,
        title: str | None = None,
    ) -> str | None:
        """
        Extract the first meaningful article section.

        The parser returns raw textual content. Semantic
        normalization belongs to the mapper.
        """

        normalized_title = (
            self._normalize_section_name(title)
            if title
            else None
        )

        headings = soup.select(
            ScholarshipsAdsSelectors.SECTION_HEADINGS,
        )

        for heading in headings:
            heading_text = heading.get_text(
                " ",
                strip=True,
            )

            section_name = (
                self._normalize_section_name(
                    heading_text,
                )
            )

            if section_name == normalized_title:
                continue

            content = self._collect_section_content(
                heading,
            )

            if content:
                return "\n\n".join(content)

        return None

    # ------------------------------------------------------------------
    # Scholarship card metadata
    # ------------------------------------------------------------------

    def _extract_card_metadata(
        self,
        soup: BeautifulSoup,
    ) -> dict[str, str | None]:
        """
        Extract raw metadata from the ScholarshipsAds card.

        Category/degree information intentionally remains here
        under `card["degree"]`.

        The mapper is responsible for converting that information
        into the normalized opportunity category.
        """

        metadata: dict[str, str | None] = {
            "funding": None,
            "organization": None,
            "degree": None,
            "subjects": None,
            "nationality": None,
            "country": None,
            "deadline": None,
        }

        icon_mapping = {
            "icon-dollor": "funding",
            "icon-place": "organization",
            "icon-Bachelor2": "degree",
            "icon-book": "subjects",
            "icon-world": "nationality",
            "icon-map": "country",
            "icon-calendar": "deadline",
        }

        for item in soup.select(
            ScholarshipsAdsSelectors.CARD_ITEMS,
        ):
            icon = item.select_one("i")

            if not icon:
                continue

            field_name = None

            for class_name in icon.get(
                "class",
                [],
            ):
                if class_name in icon_mapping:
                    field_name = icon_mapping[class_name]
                    break

            if not field_name:
                continue

            # Work on a copy so the original soup is untouched.
            item_copy = BeautifulSoup(
                str(item),
                "html.parser",
            )

            copy_icon = item_copy.select_one("i")

            if copy_icon:
                copy_icon.decompose()

            value = self._clean_text(
                item_copy.get_text(
                    " ",
                    strip=True,
                )
            )

            if value:
                metadata[field_name] = value

        return metadata

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    def _extract_application_url(
        self,
        soup: BeautifulSoup,
    ) -> str | None:
        """
        Extract the application URL.

        JavaScript/auth placeholders such as "#" are ignored.
        """

        element = soup.select_one(
            ScholarshipsAdsSelectors.APPLY_BUTTON,
        )

        if not element:
            return None

        href = element.get("href")

        if not href:
            return None

        href = href.strip()

        invalid_values = {
            "#",
            "",
            "javascript:void(0)",
            "javascript:void(0);",
        }

        if href.lower() in invalid_values:
            return None

        return href

    # ------------------------------------------------------------------
    # Published date
    # ------------------------------------------------------------------

    def _extract_published_date(
        self,
        soup: BeautifulSoup,
    ) -> str | None:
        """
        Extract the raw published date.

        Example:

            Published on: 04 Sep 2026

        Returns:

            04 Sep 2026

        Date conversion belongs to the mapper.
        """

        element = soup.select_one(
            ScholarshipsAdsSelectors.PUBLISHED_DATE,
        )

        if not element:
            return None

        text = self._clean_text(
            element.get_text(
                " ",
                strip=True,
            )
        )

        if not text:
            return None

        text = re.sub(
            r"^published\s+on\s*:\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )

        return text or None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_section_name(
        value: str | None,
    ) -> str:
        """
        Convert a heading into a clean machine-readable key.

        Examples:

            "Benefits"
                -> "benefits"

            "Step 1: Check Your Eligibility"
                -> "step_1_check_your_eligibility"

            "Study at 3 Universities: Harvard, Oxford..."
                -> "study_at_3_universities_harvard_oxford..."

            "What's the deadline?"
                -> "whats_the_deadline"
        """

        if not value:
            return ""

        value = value.strip().lower()

        # Normalize common dash characters.
        value = re.sub(
            r"[-–—−]",
            "_",
            value,
        )

        # Remove apostrophes instead of turning them
        # into underscores.
        value = re.sub(
            r"[\'’`]",
            "",
            value,
        )

        # Replace every non-alphanumeric character
        # with an underscore.
        value = re.sub(
            r"[^a-z0-9]+",
            "_",
            value,
        )

        # Collapse duplicate underscores.
        value = re.sub(
            r"_+",
            "_",
            value,
        )

        return value.strip("_")

    @staticmethod
    def _clean_text(
        value: str,
    ) -> str:
        """
        Normalize whitespace without changing the
        semantic content.
        """

        return " ".join(
            value.split()
        )

    @staticmethod
    def _text(
        soup: BeautifulSoup,
        selector: str | None,
    ) -> str | None:
        if not selector:
            return None

        element = soup.select_one(selector)

        if not element:
            return None

        text = element.get_text(
            " ",
            strip=True,
        )

        return text or None