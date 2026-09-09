import asyncio
import json

from redis.asyncio import Redis

from app.core.config import settings
from app.core.realtime import manager
from app.core.realtime.channels import REALTIME_CHANNEL


class RealtimeSubscriber:

    def __init__(self):

        self.redis = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

        self.task = None
        self.running = False

    async def start(self):

        self.running = True
        self.task = asyncio.create_task(
            self.listen()
        )

        print("✅ Realtime subscriber started")


    async def listen(self):

        self.pubsub = self.redis.pubsub()

        await self.pubsub.subscribe(
            REALTIME_CHANNEL
        )

        async for message in self.pubsub.listen():

            if message["type"] != "message":
                continue

            payload = json.loads(
                message["data"]
            )

            target = payload["target"]

            if target == "user":

                await manager.send_to_user(
                    tenant_id=payload["tenant_id"],
                    company_id=payload["company_id"],
                    branch_id=payload["branch_id"],
                    user_id=payload["user_id"],
                    message=payload["message"],
                )

            elif target == "role":

                await manager.send_to_role(
                    tenant_id=payload["tenant_id"],
                    company_id=payload["company_id"],
                    branch_id=payload["branch_id"],
                    role=payload["role"],
                    message=payload["message"],
                )

            elif target == "branch":

                await manager.send_to_branch(
                    tenant_id=payload["tenant_id"],
                    company_id=payload["company_id"],
                    branch_id=payload["branch_id"],
                    message=payload["message"],
                )

            elif target == "company":

                await manager.send_to_company(
                    tenant_id=payload["tenant_id"],
                    company_id=payload["company_id"],
                    message=payload["message"],
                )

            elif target == "tenant":

                await manager.send_to_tenant(
                    tenant_id=payload["tenant_id"],
                    message=payload["message"],
                )

            elif target == "global":

                await manager.broadcast_all(
                    payload["message"]
                )

    async def stop(self):

        self.running = False

        if self.task:
            self.task.cancel()

        if hasattr(self, "pubsub"):
            await self.pubsub.close()

        await self.redis.close()

subscriber = RealtimeSubscriber()