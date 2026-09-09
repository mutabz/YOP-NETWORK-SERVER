from collections.abc import AsyncIterator

from app.modules.opportunities.scraper.core.bases import (
    BaseFetcher,
    BaseSource,
)
from app.modules.opportunities.scraper.core.models import (
    RawOpportunity,
)
from app.modules.opportunities.scraper.core.sitemap.service import (
    SitemapService,
)

from .parser import ScholarshipsAdsParser


class ScholarshipsAdsSource(BaseSource):
    """
    ScholarshipsAds opportunity source.

    Responsible for:
        - discovering opportunity URLs through the sitemap
        - fetching opportunity pages
        - parsing pages into RawOpportunity objects

    It does not:
        - map opportunities
        - normalize fields
        - persist opportunities
    """

    name = "scholarships_ads"

    SITEMAP_URL = (
        "https://www.scholarshipsads.com/sitemap.xml"
    )

    def __init__(
        self,
        *,
        fetcher: BaseFetcher,
        sitemap_service: SitemapService,
        parser: ScholarshipsAdsParser | None = None,
        config: dict | None = None,
    ) -> None:
        super().__init__(
            source_url="https://www.scholarshipsads.com/",
            fetcher=fetcher,
            config=config,
        )

        self.sitemap_service = sitemap_service
        self.parser = parser or ScholarshipsAdsParser()

    async def scrape(
        self,
    ) -> AsyncIterator[RawOpportunity]:
        entries = await self.sitemap_service.discover(
            self.SITEMAP_URL,
        )

        for entry in entries:
            html = await self.fetcher.fetch(
                entry.url,
            )

            yield self.parser.parse(
                html,
                source_url=entry.url,
            )