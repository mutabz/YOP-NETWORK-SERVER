from app.shared.base_repository import BaseRepository
from app.modules.opportunities.models import OpportunitySource


class OpportunitySourceRepository(BaseRepository):
    model = OpportunitySource