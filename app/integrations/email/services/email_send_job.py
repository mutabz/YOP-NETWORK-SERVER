from __future__ import annotations

from uuid import UUID

from app.shared.base_service import BaseService

from app.integrations.email.repositories import (
    EmailSendJobRepository,
)

from app.integrations.email.enums import (
    EmailSendJobStatus,
)


class EmailSendJobService(BaseService):

    model_name = "email_send_job"

    create_schema = None

    def __init__(
        self,
        repository: EmailSendJobRepository,
    ):
        super().__init__(repository)

        self.repository: EmailSendJobRepository = repository

    # =========================================================
    # LOOKUPS
    # =========================================================

    async def get_by_email(
        self,
        email_id: UUID,
        select_fields=None,
    ):
        return await self.repository.get_by_email(
            email_id=email_id,
            select_fields=select_fields,
        )

    async def get_by_task_id(
        self,
        celery_task_id: str,
        select_fields=None,
    ):
        return await self.repository.get_by_task_id(
            celery_task_id=celery_task_id,
            select_fields=select_fields,
        )

    # =========================================================
    # STATUS
    # =========================================================

    async def update_status(
        self,
        job_id: UUID,
        status: EmailSendJobStatus,
    ):
        return await self.repository.update_status(
            job_id=job_id,
            status=status,
        )

    async def mark_processing(
        self,
        job_id: UUID,
    ):
        return await self.repository.mark_processing(
            job_id=job_id,
        )

    async def mark_completed(
        self,
        job_id: UUID,
    ):
        return await self.repository.mark_completed(
            job_id=job_id,
        )

    async def mark_failed(
        self,
        job_id: UUID,
        error_message: str,
    ):
        return await self.repository.mark_failed(
            job_id=job_id,
            error_message=error_message,
        )

    async def mark_cancelled(
        self,
        job_id: UUID,
    ):
        return await self.repository.mark_cancelled(
            job_id=job_id,
        )

    # =========================================================
    # ATTEMPTS
    # =========================================================

    async def increment_attempts(
        self,
        job_id: UUID,
    ):
        return await self.repository.increment_attempts(
            job_id=job_id,
        )