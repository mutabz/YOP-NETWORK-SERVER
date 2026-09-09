from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.opportunities.enums import OpportunityStatus

from app.modules.opportunities.models import Opportunity

from app.modules.opportunities.repositories import (
    OpportunityRepository,
)
from app.modules.opportunities.services import (
    OpportunityService,
)
from app.modules.opportunities.schemas import (
    OpportunityCreate,
    OpportunityUpdate,
)


router = APIRouter(prefix="/opportunities")

print("🧠 OPPORTUNITY ROUTER LOADED")


def get_service(db: AsyncSession):
    repo = OpportunityRepository(db)
    return OpportunityService(repo)


# =========================
# CREATE
# =========================

@router.post("")
@router.post("/")
async def create_opportunity(
    payload: OpportunityCreate,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return await service.create(
        **payload.model_dump()
    )


# =========================
# LIST + SEARCH
# =========================

@router.get("")
@router.get("/")
async def list_opportunities(
    search: Optional[str] = None,
    type: Optional[str] = None,
    category: Optional[str] = None,
    country: Optional[str] = None,
    status: Optional[str] = None,
    remote: Optional[bool] = None,
    page: int = 1,
    per_page: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    filters = {}
    filters["status"] = OpportunityStatus.PUBLISHED
    if type:
        filters["type"] = type

    if category:
        filters["category"] = category

    if country:
        filters["country"] = country

    if remote is not None:
        filters["remote"] = remote

    return await service.repository.list(
        filters=filters or None,
        search=search,
        search_fields=[
            "title",
            "slug",
            "slug_list",
            "category",
            "organization",
            "country",
            "city",
            "location",
            "summary",
            "description",
            "eligibility",
            "requirements",
        ],
        page=page,
        per_page=per_page,
    )

# =========================
# LIST + SEARCH
# =========================

@router.get("/admin")
async def list_opportunities(
    search: Optional[str] = None,
    type: Optional[str] = None,
    category: Optional[str] = None,
    country: Optional[str] = None,
    status: Optional[str] = None,
    remote: Optional[bool] = None,
    page: int = 1,
    per_page: int = 20,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    filters = {}

    if type:
        filters["type"] = type

    if category:
        filters["category"] = category

    if country:
        filters["country"] = country

    if status:
        filters["status"] = status

    if remote is not None:
        filters["remote"] = remote

    return await service.repository.list(
        filters=filters or None,
        search=search,
        search_fields=[
            "title",
            "slug",
            "slug_list",
            "category",
            "organization",
            "country",
            "city",
            "location",
            "summary",
            "description",
            "eligibility",
            "requirements",
        ],
        page=page,
        per_page=per_page,
    )


# =========================
# SITEMAP
# =========================

@router.get("/sitemap")
async def sitemap_opportunities(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(
            Opportunity.slug,
            Opportunity.updated_at,
            Opportunity.created_at,
        )
        .where(
            Opportunity.is_active.is_(True),
            Opportunity.slug.is_not(None),
        )
    )

    opportunities = result.all()

    return [
        {
            "slug": slug,
            "updated_at": updated_at,
            "created_at": created_at,
        }
        for slug, updated_at, created_at in opportunities
    ]


# =========================
# GET BY SLUG
# =========================

@router.get("/slug/{slug}")
async def get_opportunity_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    opportunity = await service.repository.find_by_slug(slug)

    if not opportunity:
        return None

    return opportunity


# =========================
# COUNT
# =========================

@router.get("/meta/count")
async def count_opportunities(
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return {
        "count": await service.count()
    }


# =========================
# ACTIONS
# =========================

@router.post("/{opportunity_id}/publish")
async def publish_opportunity(
    opportunity_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return await service.publish(opportunity_id)


@router.post("/{opportunity_id}/close")
async def close_opportunity(
    opportunity_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return await service.close(opportunity_id)


@router.post("/{opportunity_id}/expire")
async def expire_opportunity(
    opportunity_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return await service.expire(opportunity_id)


@router.post("/{opportunity_id}/archive")
async def archive_opportunity(
    opportunity_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return await service.archive(opportunity_id)


# =========================
# GET BY ID
# =========================

@router.get("/{opportunity_id}")
async def get_opportunity(
    opportunity_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return await service.get(opportunity_id)


# =========================
# UPDATE
# =========================

@router.put("/{opportunity_id}")
async def update_opportunity(
    opportunity_id: str,
    payload: dict,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    print(payload)

    return await service.update(
        opportunity_id,
        **payload,
    )


# =========================
# DELETE
# =========================

@router.delete("/{opportunity_id}")
async def delete_opportunity(
    opportunity_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)

    return await service.delete(opportunity_id)