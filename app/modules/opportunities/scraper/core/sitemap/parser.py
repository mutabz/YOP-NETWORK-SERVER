from datetime import datetime
from xml.etree import ElementTree

from app.modules.opportunities.scraper.core.models import (
    SitemapEntry,
    SitemapIndexEntry,
)


class SitemapParser:
    """
    Parses XML sitemap documents.

    Supports:
        - sitemap indexes
        - regular URL sitemaps
    """

    def parse_index(
        self,
        xml: str,
    ) -> list[SitemapIndexEntry]:
        """
        Parse a sitemap index.

        Returns:
            SitemapIndexEntry objects.
        """

        root = ElementTree.fromstring(xml)

        entries: list[SitemapIndexEntry] = []

        for sitemap in root:
            loc = self._find_text(
                sitemap,
                "loc",
            )

            if not loc:
                continue

            last_modified = self._parse_datetime(
                self._find_text(
                    sitemap,
                    "lastmod",
                )
            )

            entries.append(
                SitemapIndexEntry(
                    url=loc,
                    last_modified=last_modified,
                )
            )

        return entries

    def parse(
        self,
        xml: str,
    ) -> list[SitemapEntry]:
        """
        Parse a regular XML sitemap.

        Returns:
            SitemapEntry objects.
        """

        root = ElementTree.fromstring(xml)

        entries: list[SitemapEntry] = []

        for url_node in root:
            loc = self._find_text(
                url_node,
                "loc",
            )

            if not loc:
                continue

            last_modified = self._parse_datetime(
                self._find_text(
                    url_node,
                    "lastmod",
                )
            )

            change_frequency = self._find_text(
                url_node,
                "changefreq",
            )

            priority = self._parse_priority(
                self._find_text(
                    url_node,
                    "priority",
                )
            )

            entries.append(
                SitemapEntry(
                    url=loc,
                    last_modified=last_modified,
                    change_frequency=change_frequency,
                    priority=priority,
                )
            )

        return entries

    @staticmethod
    def _find_text(
        element: ElementTree.Element,
        tag: str,
    ) -> str | None:
        """
        Find an XML child while supporting sitemap namespaces.
        """

        for child in element:
            if child.tag.rsplit("}", 1)[-1] == tag:
                if child.text:
                    return child.text.strip()

        return None

    @staticmethod
    def _parse_datetime(
        value: str | None,
    ) -> datetime | None:
        """
        Parse an ISO-8601 sitemap date.
        """

        if not value:
            return None

        try:
            return datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )
        except ValueError:
            return None

    @staticmethod
    def _parse_priority(
        value: str | None,
    ) -> float | None:
        """
        Parse sitemap priority safely.
        """

        if not value:
            return None

        try:
            return float(value)
        except ValueError:
            return None