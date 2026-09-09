from app.modules.opportunities.scraper.core.bases import BaseMapper
from app.modules.opportunities.scraper.core.bases import BaseSource
from app.modules.opportunities.services import OpportunityService

from .result import ScraperResult


class ScraperOrchestrator:
    def __init__(
        self,
        *,
        source: BaseSource,
        mapper: BaseMapper,
        opportunity_service: OpportunityService,
    ) -> None:
        self.source = source
        self.mapper = mapper
        self.opportunity_service = opportunity_service

    async def run(self) -> ScraperResult:
        result = ScraperResult(
            source_name=self.source.source_url,
        )

        async for raw in self.source.scrape():
            result.discovered += 1

            try:
                mapped = self.mapper.map(raw)
                await self.opportunity_service.ingest(mapped)

                result.add_success()

            except Exception as exc:
                result.add_error(exc)

        return result
