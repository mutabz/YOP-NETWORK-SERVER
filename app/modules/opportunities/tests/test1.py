import pytest

from app.core.database import AsyncSessionLocal
from app.modules.opportunities.models import Opportunity
from app.modules.opportunities.repositories import OpportunityRepository
from app.modules.opportunities.services import OpportunityService

from app.modules.opportunities.scraper.scholarships_ads import (
    ScholarshipsAdsSource,
    ScholarshipsAdsParser,
    ScholarshipsAdsMapper,
)
from app.modules.opportunities.scraper.fetchers import HTTPFetcher
from app.modules.opportunities.scraper.core.http import HTTPClient
from app.modules.opportunities.scraper.core.sitemap import SitemapService
from app.modules.opportunities.scraper.orchestrator import ScraperOrchestrator


@pytest.mark.asyncio
async def test_real_scholarships_ads_end_to_end():
    """
    Real end-to-end scraper test.

    Uses:
        - real HTTPClient
        - real HTTPFetcher
        - real SitemapService
        - real ScholarshipsAdsSource
        - real ScholarshipsAdsParser
        - real ScholarshipsAdsMapper
        - real ScraperOrchestrator
        - real OpportunityService
        - real OpportunityRepository
        - real PostgreSQL database

    Development safety:
        Only the first 3 sitemap opportunity URLs are processed.
    """

    http_client = HTTPClient()
    fetcher = HTTPFetcher(client=http_client)


    try:
        sitemap_service = SitemapService(fetcher=fetcher)



        source = ScholarshipsAdsSource(
            fetcher=fetcher,
            sitemap_service=sitemap_service,
        )

        parser = ScholarshipsAdsParser()
        mapper = ScholarshipsAdsMapper()

        async with AsyncSessionLocal() as db:
            repository = OpportunityRepository(db)
            service = OpportunityService(repository)

            orchestrator = ScraperOrchestrator(
                source=source,
                mapper=mapper,
                opportunity_service=service,
            )


            result = await orchestrator.run()

            print("\n" + "=" * 70)
            print("SCHOLARSHIPS ADS E2E SCRAPER RESULT")
            print("=" * 70)
            print(f"Discovered : {result.discovered}")
            print(f"Processed  : {result.processed}")
            print(f"Failed     : {result.failed}")

            if result.errors:
                print("\nErrors:")
                for error in result.errors:
                    print(f"  - {error}")

            print("=" * 70)

            assert result.discovered == 3
            assert result.processed > 0
            assert result.failed == 0

            # Verify that the scraped opportunities actually exist
            # in the real database.
            for item in result.items:
                assert item.id is not None

                saved = await repository.get(item.id)

                assert saved is not None
                assert saved.source_name == item.source_name
                assert saved.source_url == item.source_url
                assert saved.title == item.title

    finally:
        await http_client.close()
