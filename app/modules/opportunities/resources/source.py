from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.modules.opportunities.repositories import (
    OpportunitySourceRepository,
)
from app.modules.opportunities.services import (
    OpportunitySourceService,
)
from app.modules.opportunities.schemas import (
    OpportunitySourceCreate,
    OpportunitySourceUpdate,
)


router = APIRouter(prefix="/opportunity-sources")

print("🧠 OPPORTUNITY SOURCE ROUTER LOADED")


def get_service(db: AsyncSession):
    repo = OpportunitySourceRepository(db)
    return OpportunitySourceService(repo)


# =========================
# CREATE
# =========================
@router.post("")
@router.post("/")
async def create_opportunity_source(
    payload: OpportunitySourceCreate,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return await service.create(
        **payload.model_dump()
    )


# =========================
# GET
# =========================
@router.get("/{source_id}")
async def get_opportunity_source(
    source_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return await service.get(source_id)


# =========================
# LIST + SEARCH
# =========================
@router.get("")
@router.get("/")
async def list_opportunity_sources(
    search: Optional[str] = None,
    source_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = 1,
    per_page: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    filters = {}

    if source_type:
        filters["source_type"] = source_type

    if is_active is not None:
        filters["is_active"] = is_active

    return await service.repository.list(
        filters=filters or None,
        search=search,
        search_fields=[
            "name",
            "url",
        ],
        page=page,
        per_page=per_page,
    )


# =========================
# UPDATE
# =========================
@router.put("/{source_id}")
async def update_opportunity_source(
    source_id: str,
    payload: OpportunitySourceUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return await service.update(
        source_id,
        **payload.model_dump(exclude_unset=True),
    )


# =========================
# DELETE
# =========================
@router.delete("/{source_id}")
async def delete_opportunity_source(
    source_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return await service.delete(source_id)


# =========================
# COUNT
# =========================
@router.get("/meta/count")
async def count_opportunity_sources(
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return {
        "count": await service.count()
    }