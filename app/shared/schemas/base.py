from pydantic import BaseModel
from typing import Optional


class BaseResponse(BaseModel):
    id: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }