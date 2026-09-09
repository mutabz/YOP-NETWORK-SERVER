from typing import Any, Optional

from pydantic import BaseModel, Field

from app.shared.schemas.base import BaseResponse

from app.modules.opportunities.enums import SourceType


class OpportunitySourceCreate(BaseModel):

    name: str
    url: str

    source_type: SourceType

    is_active: bool = True

    config: dict[str, Any] = Field(
        default_factory=dict
    )


class OpportunitySourceUpdate(BaseModel):

    name: Optional[str] = None
    url: Optional[str] = None

    source_type: Optional[SourceType] = None

    is_active: Optional[bool] = None

    config: Optional[dict[str, Any]] = None


class OpportunitySourceResponse(BaseResponse):

    name: str
    url: str

    source_type: SourceType

    is_active: bool

    config: dict[str, Any]