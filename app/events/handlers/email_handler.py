from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.worker_database import WorkerAsyncSessionLocal

from app.integrations.email.models import (
    Email,
    EmailRecipient,
    EmailAttachment,
    EmailSendJob,
)

from app.integrations.email.managers import (
    EmailDeliveryManager,
)

from app.shared.json_serialize import make_json_serializable


async def email_send_handler(payload: dict):
    """
    Handle EMAIL_SEND_REQUESTED background events.

    Responsibilities:
    - Validate event payload.
    - Open worker database session.
    - Load email and related records.
    - Delegate actual delivery to EmailDeliveryManager.
    """

    email_id = payload.get("email_id")
    send_job_id = payload.get("send_job_id")

    if not email_id:
        return

    if not send_job_id:
        return

    payload = make_json_serializable(payload)

    email_uuid = UUID(str(email_id))
    send_job_uuid = UUID(str(send_job_id))

    async with WorkerAsyncSessionLocal() as session:

        # =====================================================
        # LOAD EMAIL
        # =====================================================

        email_result = await session.execute(
            select(Email)
            .options(
                selectinload(Email.recipients),
                selectinload(Email.attachments),
            )
            .where(
                Email.id == email_uuid
            )
        )

        email = email_result.scalar_one_or_none()

        if not email:
            return

        # =====================================================
        # LOAD SEND JOB
        # =====================================================

        job_result = await session.execute(
            select(EmailSendJob)
            .where(
                EmailSendJob.id == send_job_uuid,
                EmailSendJob.email_id == email_uuid,
            )
        )

        send_job = job_result.scalar_one_or_none()

        if not send_job:
            return

        # =====================================================
        # DELIVERY MANAGER
        # =====================================================

        manager = EmailDeliveryManager(
            session=session,
        )

        await manager.deliver(
            email=email,
            send_job=send_job,
        )