from __future__ import annotations

from datetime import datetime, timezone

from app.shared.base_repository import BaseRepository

from app.integrations.email.models import (
    EmailSendJob,
)

from app.integrations.email.enums import (
    EmailSendJobStatus,
)


class EmailSendJobRepository(BaseRepository):

    model = EmailSendJob

    # =========================
    # EMAIL
    # =========================

    async def get_by_email(
        self,
        email_id,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "email_id": email_id,
            },
            select_fields=select_fields,
        )

    # =========================
    # CELERY TASK
    # =========================

    async def get_by_task_id(
        self,
        celery_task_id: str,
        select_fields=None,
    ):
        return await self.first(
            filters={
                "celery_task_id": celery_task_id,
            },
            select_fields=select_fields,
        )

    # =========================
    # STATUS
    # =========================

    async def update_status(
        self,
        job_id,
        status: EmailSendJobStatus,
    ):
        return await self.update(
            job_id,
            status=status,
        )

    async def mark_processing(
        self,
        job_id,
    ):
        return await self.update(
            job_id,
            status=EmailSendJobStatus.PROCESSING,
            started_at=datetime.now(timezone.utc),
        )

    async def mark_completed(
        self,
        job_id,
    ):
        return await self.update(
            job_id,
            status=EmailSendJobStatus.COMPLETED,
            completed_at=datetime.now(timezone.utc),
            error_message=None,
        )

    async def mark_failed(
        self,
        job_id,
        error_message: str,
    ):
        return await self.update(
            job_id,
            status=EmailSendJobStatus.FAILED,
            failed_at=datetime.now(timezone.utc),
            error_message=error_message,
        )

    async def mark_cancelled(
        self,
        job_id,
    ):
        return await self.update(
            job_id,
            status=EmailSendJobStatus.CANCELLED,
        )

    # =========================
    # ATTEMPTS
    # =========================

    async def increment_attempts(
        self,
        job_id,
    ):
        job = await self.get(job_id)

        if not job:
            return None

        return await self.update(
            job_id,
            attempts=job.attempts + 1,
        )

    # =========================
    # QUEUE
    # =========================

    async def get_pending(
        self,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "status": EmailSendJobStatus.PENDING,
            },
            sort_by="created_at",
            direction="asc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )

    async def get_failed(
        self,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "status": EmailSendJobStatus.FAILED,
            },
            sort_by="failed_at",
            direction="desc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )

    async def get_processing(
        self,
        select_fields=None,
        page: int = 1,
        per_page: int = 20,
    ):
        return await self.list(
            filters={
                "status": EmailSendJobStatus.PROCESSING,
            },
            sort_by="started_at",
            direction="asc",
            page=page,
            per_page=per_page,
            select_fields=select_fields,
        )