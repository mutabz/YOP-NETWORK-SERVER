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
        - normalize values
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
        soup = BeautifulSoup(html, "html.parser")

        sections = self._extract_sections(soup)

        return RawOpportunity(
            source_name=self.name,
            source_url=source_url,
            title=self._text(
                soup,
                ScholarshipsAdsSelectors.TITLE,
            ),
            url=source_url,
            description=self._extract_description(
                soup,
                sections,
            ),
            extras=sections,
        )

    def _extract_sections(
        self,
        soup: BeautifulSoup,
    ) -> dict[str, list[str]]:
        sections: dict[str, list[str]] = {}

        headings = soup.select(
            ScholarshipsAdsSelectors.SECTION_HEADING
        )

        for heading in headings:
            section_name = self._normalize_section_name(
                heading.get_text(" ", strip=True)
            )

            if not section_name:
                continue

            content = self._collect_section_content(
                heading
            )

            if content:
                sections[section_name] = content

        return sections

    def _collect_section_content(
        self,
        heading: Tag,
    ) -> list[str]:
        content: list[str] = []

        for sibling in heading.next_siblings:
            if not isinstance(sibling, Tag):
                continue

            if sibling.name == (
                ScholarshipsAdsSelectors.SECTION_HEADING
            ):
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

        return content

    @staticmethod
    def _extract_description(
        soup: BeautifulSoup,
        sections: dict[str, list[str]],
    ) -> str | None:
        """
        Extract the introductory content before the first
        section heading as the raw description.
        """

        first_heading = soup.select_one(
            ScholarshipsAdsSelectors.SECTION_HEADING
        )

        if not first_heading:
            return None

        description_parts: list[str] = []

        for sibling in first_heading.previous_siblings:
            if not isinstance(sibling, Tag):
                continue

            if sibling.name == "p":
                text = ScholarshipsAdsParser._clean_text(
                    sibling.get_text(
                        " ",
                        strip=True,
                    )
                )

                if text:
                    description_parts.append(text)

        description_parts.reverse()

        if description_parts:
            return "\n\n".join(
                description_parts
            )

        return None

    @staticmethod
    def _normalize_section_name(
        value: str,
    ) -> str:
        return (
            value.strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

    @staticmethod
    def _clean_text(
        value: str,
    ) -> str:
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