from __future__ import annotations

import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from app.integrations.email.models import (
    Email,
    EmailSendJob,
)

from app.integrations.email.enums import (
    EmailSendJobStatus, EmailStatus
)


class EmailDeliveryManager:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    # =========================================================
    # PUBLIC
    # =========================================================

    async def deliver(
        self,
        email: Email,
        send_job: EmailSendJob,
    ):
        """
        Deliver an email through the configured SMTP provider.

        This manager owns the actual email delivery lifecycle.
        """

        try:

            # -------------------------------------------------
            # START DELIVERY
            # -------------------------------------------------

            await self._mark_sending(
                email,
                send_job,
            )

            # -------------------------------------------------
            # BUILD MESSAGE
            # -------------------------------------------------

            message = await self._build_message(
                email
            )

            # -------------------------------------------------
            # SEND
            # -------------------------------------------------

            await self._send_smtp(
                message
            )

            # -------------------------------------------------
            # SUCCESS
            # -------------------------------------------------

            await self._mark_sent(
                email,
                send_job,
            )

        except Exception as exc:

            # -------------------------------------------------
            # FAILURE
            # -------------------------------------------------

            await self._mark_failed(
                email,
                send_job,
                str(exc),
            )

            raise

    # =========================================================
    # MESSAGE
    # =========================================================

    async def _build_message(
        self,
        email: Email,
    ) -> EmailMessage:

        message = EmailMessage()

        # -----------------------------------------------------
        # FROM
        # -----------------------------------------------------

        sender = settings.MAIL_DEFAULT_SENDER

        if sender:
            message["From"] = sender
        else:
            message["From"] = settings.MAIL_USERNAME

        # -----------------------------------------------------
        # TO / CC / BCC
        # -----------------------------------------------------

        recipients = getattr(
            email,
            "recipients",
            [],
        )

        to_addresses = []
        cc_addresses = []
        bcc_addresses = []

        for recipient in recipients:

            address = recipient.email

            if not address:
                continue

            recipient_type = str(
                recipient.recipient_type
            ).upper()

            if recipient_type.endswith("TO"):
                to_addresses.append(address)

            elif recipient_type.endswith("CC"):
                cc_addresses.append(address)

            elif recipient_type.endswith("BCC"):
                bcc_addresses.append(address)

        if to_addresses:
            message["To"] = ", ".join(
                to_addresses
            )

        if cc_addresses:
            message["Cc"] = ", ".join(
                cc_addresses
            )

        if bcc_addresses:
            message["Bcc"] = ", ".join(
                bcc_addresses
            )

        # -----------------------------------------------------
        # SUBJECT
        # -----------------------------------------------------

        message["Subject"] = email.subject

        # -----------------------------------------------------
        # BODY
        # -----------------------------------------------------

        html_body = getattr(
            email,
            "html_body",
            None,
        )

        text_body = getattr(
            email,
            "text_body",
            None,
        )

        if html_body:

            message.set_content(
                text_body or ""
            )

            message.add_alternative(
                html_body,
                subtype="html",
            )

        else:

            message.set_content(
                text_body or ""
            )

        # -----------------------------------------------------
        # MESSAGE ID
        # -----------------------------------------------------

        if getattr(
            email,
            "message_id",
            None,
        ):
            message["Message-ID"] = email.message_id

        return message

    # =========================================================
    # SMTP
    # =========================================================

    async def _send_smtp(
        self,
        message: EmailMessage,
    ):
        """
        Send the prepared MIME message through SMTP.

        SMTP is synchronous, so this currently executes
        directly. We can move this into an executor later
        if required.
        """

        if settings.MAIL_USE_SSL:

            with smtplib.SMTP_SSL(
                settings.MAIL_SERVER,
                settings.MAIL_PORT,
            ) as smtp:

                smtp.login(
                    settings.MAIL_USERNAME,
                    settings.MAIL_PASSWORD,
                )

                smtp.send_message(
                    message
                )

            return

        with smtplib.SMTP(
            settings.MAIL_SERVER,
            settings.MAIL_PORT,
        ) as smtp:

            smtp.ehlo()

            if settings.MAIL_USE_TLS:
                smtp.starttls()
                smtp.ehlo()

            smtp.login(
                settings.MAIL_USERNAME,
                settings.MAIL_PASSWORD,
            )

            smtp.send_message(
                message
            )

    # =========================================================
    # STATUS
    # =========================================================

    async def _mark_sending(
        self,
        email: Email,
        send_job: EmailSendJob,
    ):

        email.status = EmailStatus.SENDING

        send_job.status = (
            EmailSendJobStatus.PROCESSING
        )

        send_job.attempts = (
            send_job.attempts + 1
        )

        await self.session.commit()

    # =========================================================
    # SUCCESS
    # =========================================================

    async def _mark_sent(
        self,
        email: Email,
        send_job: EmailSendJob,
    ):

        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)

        email.status = EmailStatus.SENT
        email.sent_at = now
        email.error_message = None

        send_job.status = (
            EmailSendJobStatus.COMPLETED
        )

        send_job.completed_at = now
        send_job.error_message = None

        await self.session.commit()

    # =========================================================
    # FAILURE
    # =========================================================

    async def _mark_failed(
        self,
        email: Email,
        send_job: EmailSendJob,
        error_message: str,
    ):

        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)

        email.status = EmailStatus.FAILED
        email.failed_at = now
        email.error_message = error_message

        send_job.status = (
            EmailSendJobStatus.FAILED
        )

        send_job.failed_at = now
        send_job.error_message = error_message

        await self.session.commit()