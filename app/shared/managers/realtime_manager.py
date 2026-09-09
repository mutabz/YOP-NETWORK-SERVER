from app.core.realtime import manager


class RealtimeManager:

    @staticmethod
    async def emit_to_user(
        tenant_id,
        branch_id,
        user_id,
        event_type,
        data
    ):
        await manager.emit(
            tenant_id,
            branch_id,
            user_id,
            event_type,
            data
        )

    @staticmethod
    async def emit_to_branch(
        tenant_id,
        branch_id,
        event_type,
        data
    ):
        await manager.send_to_branch(
            tenant_id,
            branch_id,
            {
                "type": event_type,
                "data": data
            }
        )

    @staticmethod
    async def emit_to_tenant(
        tenant_id,
        event_type,
        data
    ):
        await manager.send_to_tenant(
            tenant_id,
            {
                "type": event_type,
                "data": data
            }
        )