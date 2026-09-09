from app.core.realtime import manager


class RealtimeEmitter:

    @staticmethod
    async def emit_to_user(
        tenant_id,
        branch_id,
        user_id,
        event,
        data
    ):

        await manager.emit(
            tenant_id,
            branch_id,
            user_id,
            event,
            data
        )

    @staticmethod
    async def emit_to_role(
        tenant_id,
        branch_id,
        role,
        event,
        data
    ):

        await manager.send_to_role(
            tenant_id,
            branch_id,
            role,
            {
                "event": event,
                "data": data
            }
        )

    @staticmethod
    async def emit_to_tenant(
        tenant_id,
        event,
        data
    ):

        await manager.send_to_tenant(
            tenant_id,
            {
                "event": event,
                "data": data
            }
        )


realtime = RealtimeEmitter()