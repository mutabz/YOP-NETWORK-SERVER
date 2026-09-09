import asyncio

from datetime import datetime, timezone, timedelta


class HeartbeatService:

    def __init__(self, manager):
        self.manager = manager
        self.running = False
        self.task = None

    # =====================================================
    # START
    # =====================================================

    async def start(self):
        print("💓 Heartbeat Service Started")
        self.running = True
        self.task = asyncio.create_task(self.monitor())

    # =====================================================
    # STOP
    # =====================================================

    async def stop(self):
        self.running = False

        if self.task:
            self.task.cancel()

    # =====================================================
    # LOOP
    # =====================================================

    async def monitor(self):

        while self.running:

            await asyncio.sleep(60)

            await self.check_connections()

    # =====================================================
    # CHECK CONNECTIONS
    # =====================================================

    async def check_connections(self):

        timeout = (
            datetime.now(timezone.utc)
            - timedelta(seconds=90)
        )

        dead_connections = []

        for tenant_id, companies in self.manager.active_connections.items():

            for company_id, branches in companies.items():

                for branch_id, users in branches.items():

                    for user_id, connections in users.items():

                        for connection_id, connection in connections.items():

                            if connection["last_ping"] < timeout:

                                dead_connections.append(
                                    (
                                        tenant_id,
                                        company_id,
                                        branch_id,
                                        user_id,
                                        connection_id,
                                    )
                                )

        for (
            tenant_id,
            company_id,
            branch_id,
            user_id,
            connection_id,
        ) in dead_connections:

            await self.manager.unregister(
                tenant_id=tenant_id,
                company_id=company_id,
                branch_id=branch_id,
                user_id=user_id,
                connection_id=connection_id,
            )

            print(
                f"💀 Removed dead socket "
                f"{tenant_id}/{company_id}/{branch_id}/{user_id}/{connection_id}"
            )