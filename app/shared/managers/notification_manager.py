from app.services.dispatcher import TaskDispatcher


class NotificationManager:

    @staticmethod
    def email(
        tenant_id,
        email,
        subject,
        message
    ):
        TaskDispatcher.send_email(
            tenant_id,
            email,
            subject,
            message
        )

    @staticmethod
    def sms(
        tenant_id,
        phone,
        message
    ):
        TaskDispatcher.send_sms(
            tenant_id,
            phone,
            message
        )