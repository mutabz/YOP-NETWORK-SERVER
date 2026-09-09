from app.core.realtime.publisher import publisher
from app.core.realtime.events import RealtimeEvent


async def ping(
    *,
    user: dict,
    data: dict,
):

    await publisher.to_user(
        tenant_id=user["tenant_id"],
        company_id=user["company_id"],
        branch_id=user["branch_id"],
        user_id=user["user_id"],
        event=RealtimeEvent.PONG,
        data={},
    )