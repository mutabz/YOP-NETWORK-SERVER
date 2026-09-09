import asyncio

from app.modules.opportunities.scraper.core.http.client import HTTPClient
from app.modules.opportunities.scraper.core.sitemap.service import (
    SitemapService,
)
from app.modules.opportunities.scraper.fetchers.http import HTTPFetcher
from app.modules.opportunities.scraper.scholarships_ads.mapper import (
    ScholarshipsAdsMapper,
)
from app.modules.opportunities.scraper.scholarships_ads.parser import (
    ScholarshipsAdsParser,
)
from app.modules.opportunities.scraper.scholarships_ads.source import (
    ScholarshipsAdsSource,
)


SITEMAP_URL = (
    "https://www.scholarshipsads.com/sitemap.xml"
)

MAX_OPPORTUNITIES = 3


async def main() -> None:
    print("=" * 80)
    print("ScholarshipsAds COMPLETE ONLINE PIPELINE TEST")
    print("=" * 80)

    async with HTTPClient(timeout=30.0) as client:

        # ---------------------------------------------------------
        # Infrastructure
        # ---------------------------------------------------------

        fetcher = HTTPFetcher(
            client=client,
        )

        sitemap_service = SitemapService(
            fetcher=fetcher,
        )

        parser = ScholarshipsAdsParser()

        mapper = ScholarshipsAdsMapper()

        source = ScholarshipsAdsSource(
            fetcher=fetcher,
            sitemap_service=sitemap_service,
            parser=parser,
        )

        # ---------------------------------------------------------
        # 1. Sitemap discovery
        # ---------------------------------------------------------

        print("\n[1] Discovering sitemap URLs...")
        print(f"    {SITEMAP_URL}")

        entries = await sitemap_service.discover(
            SITEMAP_URL,
        )

        print(
            f"\n    Discovered opportunity URLs: "
            f"{len(entries)}"
        )

        if not entries:
            print("    ❌ No sitemap entries discovered.")
            return

        print("    ✅ Sitemap discovery works.")

        # ---------------------------------------------------------
        # 2. Show first sitemap entries
        # ---------------------------------------------------------

        print("\n[2] First sitemap entries:")

        for index, entry in enumerate(
            entries[:5],
            start=1,
        ):
            print(f"\n    {index}. {entry.url}")
            print(
                f"       Last modified: "
                f"{entry.last_modified}"
            )
            print(
                f"       Change frequency: "
                f"{entry.change_frequency}"
            )
            print(
                f"       Priority: "
                f"{entry.priority}"
            )

        # ---------------------------------------------------------
        # 3. Source → Parser → RawOpportunity
        # ---------------------------------------------------------

        print(
            "\n[3] Fetching, parsing and mapping "
            f"first {MAX_OPPORTUNITIES} opportunities..."
        )

        count = 0

        async for raw in source.scrape():

            count += 1

            print("\n" + "-" * 80)
            print(f"OPPORTUNITY #{count}")
            print("-" * 80)

            # -----------------------------------------------------
            # RawOpportunity
            # -----------------------------------------------------

            print("\nRAW OPPORTUNITY")

            print(f"  Source:       {raw.source_name}")
            print(f"  Source URL:   {raw.source_url}")
            print(f"  Title:        {raw.title}")
            print(f"  URL:          {raw.url}")
            print(f"  Organization: {raw.organization}")
            print(f"  Country:      {raw.country}")
            print(f"  Location:     {raw.location}")
            print(f"  Type:         {raw.type}")
            print(f"  Category:     {raw.category}")
            print(f"  Deadline:     {raw.deadline}")
            print(f"  Published:    {raw.published_at}")
            print(
                f"  Application:  "
                f"{raw.application_url}"
            )

            print(
                f"  Description:  "
                f"{'YES' if raw.description else 'NO'}"
            )

            print(
                f"  Extras keys:  "
                f"{list(raw.extras.keys())}"
            )

            # -----------------------------------------------------
            # Mapper
            # -----------------------------------------------------

            mapped = mapper.map(raw)

            # -----------------------------------------------------
            # MappedOpportunity
            # -----------------------------------------------------

            print("\nMAPPED OPPORTUNITY")

            print(f"  Title:        {mapped.title}")
            print(f"  Type:         {mapped.type}")
            print(f"  Category:     {mapped.category}")
            print(
                f"  Organization: "
                f"{mapped.organization}"
            )
            print(f"  Country:      {mapped.country}")
            print(f"  City:         {mapped.city}")
            print(f"  Location:     {mapped.location}")
            print(f"  Remote:       {mapped.remote}")

            print(
                f"  Deadline:     "
                f"{mapped.deadline}"
            )

            print(
                f"  Start date:   "
                f"{mapped.start_date}"
            )

            print(
                f"  End date:     "
                f"{mapped.end_date}"
            )

            print(
                f"  Published:    "
                f"{mapped.published_at}"
            )

            print(
                f"  Application:  "
                f"{mapped.application_url}"
            )

            print(
                f"  Source URL:   "
                f"{mapped.source_url}"
            )

            print(
                f"  Source name:  "
                f"{mapped.source_name}"
            )

            print(
                f"  Summary:      "
                f"{'YES' if mapped.summary else 'NO'}"
            )

            print(
                f"  Description:  "
                f"{'YES' if mapped.description else 'NO'}"
            )

            print(
                f"  Eligibility:  "
                f"{'YES' if mapped.eligibility else 'NO'}"
            )

            print(
                f"  Requirements: "
                f"{'YES' if mapped.requirements else 'NO'}"
            )

            print(
                f"  Extras keys:  "
                f"{list(mapped.extras.keys())}"
            )

            # -----------------------------------------------------
            # Basic validation
            # -----------------------------------------------------

            assert mapped.title
            assert mapped.type
            assert mapped.source_url
            assert mapped.source_name

            print("\n  ✅ Raw → Mapped successful.")

            if count >= MAX_OPPORTUNITIES:
                break

        # ---------------------------------------------------------
        # Final result
        # ---------------------------------------------------------

        print("\n" + "=" * 80)
        print(
            f"✅ SUCCESS — complete pipeline processed "
            f"{count} online opportunities."
        )
        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())