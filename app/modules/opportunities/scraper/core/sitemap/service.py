from app.modules.opportunities.scraper.core.bases import (
    BaseFetcher,
)
from app.modules.opportunities.scraper.core.models.sitemap import (
    SitemapEntry,
    SitemapIndexEntry,
)

from .parser import SitemapParser


class SitemapService:
    """
    Coordinates sitemap fetching and parsing.

    Responsibilities:
        - fetch sitemap documents
        - determine sitemap type
        - parse sitemap documents
        - expose discovered URLs

    It does not:
        - parse opportunity pages
        - map opportunities
        - know about individual sources
    """

    def __init__(
        self,
        *,
        fetcher: BaseFetcher,
        parser: SitemapParser | None = None,
    ) -> None:
        self.fetcher = fetcher
        self.parser = parser or SitemapParser()

    async def fetch(
        self,
        url: str,
    ) -> str:
        return await self.fetcher.fetch(url)

    async def parse(
        self,
        url: str,
    ) -> list[SitemapEntry]:
        xml = await self.fetch(url)

        return self.parser.parse(xml)

    async def parse_index(
        self,
        url: str,
    ) -> list[SitemapIndexEntry]:
        xml = await self.fetch(url)

        return self.parser.parse_index(xml)

    async def discover(
        self,
        url: str,
    ) -> list[SitemapEntry]:
        xml = await self.fetch(url)

        if self._is_index(xml):
            return await self._discover_from_index(xml)

        return self.parser.parse(xml)

    async def _discover_from_index(
        self,
        xml: str,
    ) -> list[SitemapEntry]:
        sitemap_entries = self.parser.parse_index(xml)

        results: list[SitemapEntry] = []

        for sitemap in sitemap_entries:
            entries = await self.parse(sitemap.url)
            results.extend(entries)

        return results

    @staticmethod
    def _is_index(
        xml: str,
    ) -> bool:
        from xml.etree import ElementTree

        root = ElementTree.fromstring(xml)

        return (
            root.tag.rsplit("}", 1)[-1]
            == "sitemapindex"
        )