from fastapi import APIRouter, Request
from fastapi.routing import APIRoute

from app.modules.opportunities.resources import (
    opportunity_router,
    opportunity_source_router,
)


router = APIRouter()


router.include_router(
    opportunity_router,
    tags=["Opportunity Routes"],
)

router.include_router(
    opportunity_source_router,
    tags=["Opportunity Source Routes"],
)