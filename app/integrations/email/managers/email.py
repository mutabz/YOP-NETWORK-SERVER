from __future__ import annotations

from typing import Any
from uuid import UUID

from jinja2 import Environment, StrictUndefined

from app.shared.managers.background_manager import (
    BackgroundManager,
)
from app.integrations.email.repositories import (
    EmailRepository,
    EmailTemplateRepository,
    EmailRecipientRepository,
    EmailAttachmentRepository,
    EmailSendJobRepository,
)
from app.integrations.email.services import (
    EmailService,
    EmailTemplateService,
    EmailSendJobService,
    EmailRecipientService,
    EmailAttachmentService,
)

from app.integrations.email.enums import (
    EmailStatus,
    EmailTemplateCode,
)

from app.events.event_types import EventType
from sqlalchemy.ext.asyncio import AsyncSession


class EmailManager:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

        # =====================================================
        # REPOSITORIES
        # =====================================================

        email_repository = EmailRepository(session)
        template_repository = EmailTemplateRepository(session)
        recipient_repository = EmailRecipientRepository(session)
        attachment_repository = EmailAttachmentRepository(session)
        send_job_repository = EmailSendJobRepository(session)

        # =====================================================
        # SERVICES
        # =====================================================

        self.email_service = EmailService(
            email_repository
        )

        self.email_template_service = EmailTemplateService(
            template_repository
        )

        self.recipient_service = EmailRecipientService(
            recipient_repository
        )

        self.attachment_service = EmailAttachmentService(
            attachment_repository
        )

        self.send_job_service = EmailSendJobService(
            send_job_repository
        )

    # =========================================================
    # QUEUE
    # =========================================================

    async def queue(
        self,
        email_id: UUID,
    ):
        email = await self.email_service.get(email_id)

        if not email:
            raise ValueError(
                "Email not found."
            )

        if email.status != EmailStatus.PENDING:
            raise ValueError(
                f"Email cannot be queued "
                f"from status {email.status}."
            )

        # -----------------------------------------------------
        # Create send job
        # -----------------------------------------------------

        job = await self.send_job_service.create(
            email_id=email.id,
        )

        # -----------------------------------------------------
        # Publish background event
        # -----------------------------------------------------

        BackgroundManager.publish(
            event_type=EventType.EMAIL_SEND_REQUESTED,
            payload={
                "email_id": str(email.id),
                "send_job_id": str(job.id),
            },
        )

        return job


    # =========================================================
    # SEND TEMPLATE
    # =========================================================

    async def send_template(
        self,
        template_code: EmailTemplateCode,
        context: dict[str, Any],
        recipients: list[dict],
        *,
        attachments: list[dict] | None = None,
        priority=None,
        extra_metadata: dict | None = None,
    ):
        """
        Create an email from a stored system email template
        and queue it for asynchronous delivery.
        """

        # =====================================================
        # 1. LOAD TEMPLATE
        # =====================================================

        template = await self.email_template_service.get_by_code(
            template_code.value,
        )

        if not template:
            raise ValueError(
                f"Email template "
                f"'{template_code.value}' not found."
            )

        # =====================================================
        # 2. VALIDATE TEMPLATE
        # =====================================================

        if not template.is_active:
            raise ValueError(
                f"Email template "
                f"'{template_code.value}' is inactive."
            )

        if not template.published_at:
            raise ValueError(
                f"Email template "
                f"'{template_code.value}' "
                f"has not been published."
            )

        # =====================================================
        # 3. RENDER TEMPLATE
        # =====================================================

        rendered = self._render_template(
            template=template,
            context=context,
        )

        # =====================================================
        # 4. CREATE EMAIL
        # =====================================================

        email = await self.email_service.create(
            subject=rendered["subject"],
            html_body=rendered["html_body"],
            text_body=rendered["text_body"],
            status=EmailStatus.PENDING,
            template_id=template.id,
            template_version=template.version,
            priority=priority,
            extra_metadata=extra_metadata,
        )

        # =====================================================
        # 5. CREATE RECIPIENTS
        # =====================================================

        for recipient in recipients:

            await self.recipient_service.create(
                email_id=email.id,
                **recipient,
            )

        # =====================================================
        # 6. CREATE ATTACHMENTS
        # =====================================================

        for attachment in attachments or []:

            await self.attachment_service.create(
                email_id=email.id,
                **attachment,
            )

        # =====================================================
        # 7. QUEUE
        # =====================================================

        job = await self.queue(
            email.id,
        )

        return {
            "email": email,
            "send_job": job,
        }


    # =========================================================
    # TEMPLATE RENDERER
    # =========================================================

    def _render_template(
        self,
        template,
        context: dict[str, Any],
    ) -> dict[str, str | None]:

        environment = Environment(
            undefined=StrictUndefined,
            autoescape=True,
        )

        # -----------------------------------------------------
        # Subject
        # -----------------------------------------------------

        subject = environment.from_string(
            template.subject_template
        ).render(
            **context
        )

        # -----------------------------------------------------
        # HTML
        # -----------------------------------------------------

        html_body = environment.from_string(
            template.html_template
        ).render(
            **context
        )

        # -----------------------------------------------------
        # Plain text
        # -----------------------------------------------------

        text_body = None

        if template.text_template:

            text_body = environment.from_string(
                template.text_template
            ).render(
                **context
            )

        return {
            "subject": subject,
            "html_body": html_body,
            "text_body": text_body,
        }