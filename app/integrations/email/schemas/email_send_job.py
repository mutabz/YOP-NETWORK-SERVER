from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


# ============================================================
# CREATE
# ============================================================

class EmailSendJobCreate(BaseModel):

    email_id: UUID

    priority: str | None = None 
    queue_name: str = "emails"

    max_attempts: int = 3


# ============================================================
# RESPONSE
# ============================================================

class EmailSendJobResponse(BaseModel):

    id: UUID

    email_id: UUID

    status: str | None = None

    priority: str | None = None

    queue_name: str

    celery_task_id: str | None

    attempts: int

    max_attempts: int

    started_at: datetime | None

    completed_at: datetime | None

    failed_at: datetime | None

    error_message: str | None

    created_at: datetime

    updated_at: datetime | None

    model_config = {
        "from_attributes": True,
    }


# ============================================================
# LIST ITEM
# ============================================================

class EmailSendJobListItem(BaseModel):

    id: UUID

    email_id: UUID

    status: str | None = None

    priority: str | None = None

    queue_name: str

    attempts: int

    max_attempts: int

    started_at: datetime | None

    completed_at: datetime | None

    failed_at: datetime | None

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }