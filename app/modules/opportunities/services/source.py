from app.shared.base_service import BaseService

from app.modules.opportunities.repositories import (
    OpportunitySourceRepository,
)
from app.modules.opportunities.schemas import (
    OpportunitySourceCreate,
    OpportunitySourceUpdate,
)


class OpportunitySourceService(BaseService):

    model_name = "opportunity_sources"

    create_schema = OpportunitySourceCreate
    update_schema = OpportunitySourceUpdate

    def __init__(self, repository: OpportunitySourceRepository):
        super().__init__(repository)

    async def before_create(self, data: dict):

        name = data.get("name")
        url = data.get("url")

        if name:
            data["name"] = name.strip()

        if url:
            data["url"] = url.strip()

        # Prevent duplicate source name
        if name:
            existing = await self.repository.first(
                filters={
                    "name": data["name"],
                }
            )

            if existing:
                raise ValueError(
                    "Opportunity source with this name already exists"
                )

        # Prevent duplicate source URL
        if url:
            existing = await self.repository.first(
                filters={
                    "url": data["url"],
                }
            )

            if existing:
                raise ValueError(
                    "Opportunity source with this URL already exists"
                )

        return data