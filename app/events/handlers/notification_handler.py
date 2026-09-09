from app.core.worker_database import WorkerAsyncSessionLocal
from app.shared.json_serialize import make_json_serializable

from app.modules.system_layer.system.notifications.repositories.notification import (
    NotificationRepository
)

from app.modules.system_layer.system.notifications.services.notification import (
    NotificationService
)


async def notification_handler(payload):

    print('+++\n' *5)
    print("We are into notification handler")
    print(payload)
    print('+++\n' *5)

    payload = {
        key: value
        for key, value in payload.items()
        if key not in ("event", "timestamp")
    }
    payload = make_json_serializable(payload)
    async with WorkerAsyncSessionLocal() as db:

        try:
            notification_repository = NotificationRepository(db)

            notification_service = NotificationService(
                notification_repository
            )

            await notification_service.create(payload)

            await db.commit()

        except Exception:
            await db.rollback()
            raise