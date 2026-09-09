import json

from redis.asyncio import Redis

from app.core.config import settings
from app.core.realtime.channels import REALTIME_CHANNEL


class RealtimePublisher:
    """
    Publishes realtime events to Redis.

    FastAPI websocket server subscribes to this
    channel and forwards events to connected users.

    Never talks directly to ConnectionManager.
    """



    # =====================================================
    # INTERNAL
    # =====================================================

    async def _publish(self, payload):

        redis = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

        try:
            await redis.publish(
                REALTIME_CHANNEL,
                json.dumps(payload),
            )
        finally:
            await redis.aclose()

    # =====================================================
    # USER
    # =====================================================

    async def to_user(
        self,
        *,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        user_id: str,
        event: str,
        data: dict,
    ):

        await self._publish(
            {
                "target": "user",
                "tenant_id": tenant_id,
                "company_id": company_id,
                "branch_id": branch_id,
                "user_id": user_id,
                "message": {
                    "event": event,
                    "data": data,
                },
            }
        )

    # =====================================================
    # ROLE
    # =====================================================

    async def to_role(
        self,
        *,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        role: str,
        event: str,
        data: dict,
    ):

        await self._publish(
            {
                "target": "role",
                "tenant_id": tenant_id,
                "company_id": company_id,
                "branch_id": branch_id,
                "role": role,
                "message": {
                    "event": event,
                    "data": data,
                },
            }
        )

    # =====================================================
    # BRANCH
    # =====================================================

    async def to_branch(
        self,
        *,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        event: str,
        data: dict,
    ):

        await self._publish(
            {
                "target": "branch",
                "tenant_id": tenant_id,
                "company_id": company_id,
                "branch_id": branch_id,
                "message": {
                    "event": event,
                    "data": data,
                },
            }
        )

    # =====================================================
    # COMPANY
    # =====================================================

    async def to_company(
        self,
        *,
        tenant_id: str,
        company_id: str,
        event: str,
        data: dict,
    ):

        await self._publish(
            {
                "target": "company",
                "tenant_id": tenant_id,
                "company_id": company_id,
                "message": {
                    "event": event,
                    "data": data,
                },
            }
        )

    # =====================================================
    # TENANT
    # =====================================================

    async def to_tenant(
        self,
        *,
        tenant_id: str,
        event: str,
        data: dict,
    ):

        await self._publish(
            {
                "target": "tenant",
                "tenant_id": tenant_id,
                "message": {
                    "event": event,
                    "data": data,
                },
            }
        )

    # =====================================================
    # GLOBAL
    # =====================================================

    async def broadcast(
        self,
        *,
        event: str,
        data: dict,
    ):

        await self._publish(
            {
                "target": "global",
                "message": {
                    "event": event,
                    "data": data,
                },
            }
        )

    async def close(self):
        await self.redis.close()

publisher = RealtimePublisher()