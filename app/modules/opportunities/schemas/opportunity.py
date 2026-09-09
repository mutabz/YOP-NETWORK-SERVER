from typing import Any, Optional

from pydantic import BaseModel

from app.shared.schemas.base import BaseResponse

from app.modules.opportunities.enums import (
    OpportunityStatus,
    OpportunityType,
)


class OpportunityCreate(BaseModel):

    title: str
    slug: str

    type: OpportunityType
    category: Optional[str] = None

    organization: Optional[str] = None

    country: Optional[str] = None
    city: Optional[str] = None
    location: Optional[str] = None
    remote: bool = False

    deadline: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    summary: Optional[list[Any]] = None
    description: Optional[list[Any]] = None
    eligibility: Optional[list[Any]] = None
    requirements: Optional[list[Any]] = None

    application_url: Optional[str] = None

    source_url: str
    source_name: Optional[str] = None

    status: OpportunityStatus = OpportunityStatus.DRAFT

    slug_list: list[str] = []
    extras: dict[str, Any] = {}


class OpportunityUpdate(BaseModel):

    title: Optional[str] = None
    slug: Optional[str] = None

    type: Optional[OpportunityType] = None
    category: Optional[str] = None

    organization: Optional[str] = None

    country: Optional[str] = None
    city: Optional[str] = None
    location: Optional[str] = None
    remote: Optional[bool] = None

    deadline: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    published_at: Optional[str] = None

    summary: Optional[list[Any]] = None
    description: Optional[list[Any]] = None
    eligibility: Optional[list[Any]] = None
    requirements: Optional[list[Any]] = None

    application_url: Optional[str] = None

    source_url: Optional[str] = None
    source_name: Optional[str] = None

    status: Optional[OpportunityStatus] = None

    slug_list: Optional[list[str]] = None
    extras: Optional[dict[str, Any]] = None


class OpportunityResponse(BaseResponse):

    title: str
    slug: str

    type: OpportunityType
    category: Optional[str] = None

    organization: Optional[str] = None

    country: Optional[str] = None
    city: Optional[str] = None
    location: Optional[str] = None
    remote: bool

    deadline: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    summary: Optional[list[Any]] = None
    description: Optional[list[Any]] = None
    eligibility: Optional[list[Any]] = None
    requirements: Optional[list[Any]] = None

    application_url: Optional[str] = None

    source_url: str
    source_name: Optional[str] = None

    status: OpportunityStatus

    slug_list: list[str]
    extras: dict[str, Any]