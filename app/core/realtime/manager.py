from typing import Dict, TypedDict
from fastapi import WebSocket
from datetime import datetime, timezone

import asyncio
import uuid


# =====================================================
# CONNECTION DATA
# =====================================================

class ConnectionInfo(TypedDict):

    ws: WebSocket
    user_id: str
    tenant_id: str
    company_id: str
    branch_id: str
    role: str
    connected_at: datetime
    last_ping: datetime
    device: str | None


# =====================================================
# CONNECTION MANAGER
# =====================================================

class ConnectionManager:


    def __init__(self):

        self.active_connections: Dict[
            str,  # tenant
            Dict[
                str,  # company
                Dict[
                    str,  # branch
                    Dict[
                        str,  # user
                        Dict[
                            str,  # connection_id
                            ConnectionInfo
                        ]
                    ]
                ]
            ]
        ] = {}

        self.lock = asyncio.Lock()



    # =================================================
    # START / STOP
    # =================================================


    async def start(self):

        print(
            "✅ WebSocket Manager Started"
        )


    async def stop(self):

        async with self.lock:

            for tenant in self.active_connections.values():

                for company in tenant.values():

                    for branch in company.values():

                        for user in branch.values():

                            for connection in user.values():

                                try:
                                    await connection["ws"].close()
                                except Exception:
                                    pass

            self.active_connections.clear()

        print("🛑 WebSocket Manager Stopped")


    # =================================================
    # REGISTER
    # =================================================

    async def register(
        self,
        websocket: WebSocket,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        user_id: str,
        role: str = "user",
        device: str | None = None,
    ):

        async with self.lock:
            connection_id = str(uuid.uuid4())

            self.active_connections.setdefault(tenant_id, {})
            self.active_connections[tenant_id].setdefault(company_id, {})
            self.active_connections[tenant_id][company_id].setdefault(branch_id, {})
            self.active_connections[tenant_id][company_id][branch_id].setdefault(user_id, {})

            now = datetime.now(timezone.utc)

            self.active_connections[ tenant_id ][ company_id ][ branch_id ][ user_id ][ connection_id ] = {
                "ws": websocket,
                "user_id": user_id,
                "tenant_id": tenant_id,
                "company_id": company_id,
                "branch_id": branch_id,
                "role": role,
                "connected_at": now,
                "last_ping": now,
                "device": device,
            }
            return connection_id



    # =================================================
    # UNREGISTER
    # =================================================

    async def unregister(
        self,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        user_id: str,
        connection_id: str,
    ):

        async with self.lock:

            try:

                del self.active_connections[
                    tenant_id
                ][
                    company_id
                ][
                    branch_id
                ][
                    user_id
                ][
                    connection_id
                ]

                if not self.active_connections[tenant_id][company_id][branch_id][user_id]:
                    del self.active_connections[tenant_id][company_id][branch_id][user_id]

                if not self.active_connections[tenant_id][company_id][branch_id]:
                    del self.active_connections[tenant_id][company_id][branch_id]

                if not self.active_connections[tenant_id][company_id]:
                    del self.active_connections[tenant_id][company_id]

                if not self.active_connections[tenant_id]:
                    del self.active_connections[tenant_id]

            except KeyError:
                pass


    # =================================================
    # SAFE SEND
    # =================================================


    async def _safe_send(
        self,
        websocket: WebSocket,
        message: dict
    ):


        try:

            await websocket.send_json(
                message
            )

            return True


        except Exception:

            return False



    # =================================================
    # INTERNAL BROADCAST
    # =================================================


    async def _broadcast(
        self,
        connections,
        message: dict
    ):


        if not connections:
            return


        tasks = [

            self._safe_send(
                connection["ws"],
                message
            )

            for connection in connections

        ]


        await asyncio.gather(
            *tasks,
            return_exceptions=True
        )



    # =================================================
    # USER
    # =================================================


    async def send_to_user(
        self,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        user_id: str,
        message: dict,
    ):

        try:

            connections = self.active_connections[ tenant_id ][ company_id ][ branch_id ][ user_id ]

            await self._broadcast( list(connections.values()), message, )

        except Exception as e:
            raise e


    # =================================================
    # BRANCH
    # =================================================
    
    async def send_to_company(
        self,
        tenant_id: str,
        company_id: str,
        message: dict,
    ):

        try:

            company = self.active_connections[
                tenant_id
            ][
                company_id
            ]

            connections = []

            for branch in company.values():
                for user in branch.values():
                    connections.extend(user.values())

            await self._broadcast(
                connections,
                message,
            )

        except KeyError:
            pass

    # =================================================
    # BRANCH
    # =================================================

    async def send_to_branch(
        self,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        message: dict,
    ):

        try:

            branch = self.active_connections[
                tenant_id
            ][
                company_id
            ][
                branch_id
            ]

            connections = []

            for user in branch.values():
                connections.extend(user.values())

            await self._broadcast(
                connections,
                message,
            )

        except KeyError:
            pass

    # =================================================
    # TENANT
    # =================================================

    async def send_to_tenant(
        self,
        tenant_id: str,
        message: dict,
    ):

        try:

            connections = []

            tenant = self.active_connections[tenant_id]

            for company in tenant.values():
                for branch in company.values():
                    for user in branch.values():
                        connections.extend(user.values())

            await self._broadcast(
                connections,
                message,
            )

        except KeyError:
            pass

    # =================================================
    # ROLE
    # =================================================

    async def send_to_role(
        self,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        role: str,
        message: dict,
    ):

        try:

            branch = self.active_connections[
                tenant_id
            ][
                company_id
            ][
                branch_id
            ]

            connections = []

            for user in branch.values():

                for connection in user.values():

                    if connection["role"] == role:
                        connections.append(connection)

            await self._broadcast(
                connections,
                message,
            )

        except KeyError:
            pass

    # =================================================
    # GLOBAL
    # =================================================


    async def broadcast_all(
        self,
        message: dict,
    ):

        connections = []

        for tenant in self.active_connections.values():
            for company in tenant.values():
                for branch in company.values():
                    for user in branch.values():
                        connections.extend(user.values())

        await self._broadcast(
            connections,
            message,
        )


    # =================================================
    # STATS
    # =================================================


    def stats(self):

        tenants = len(self.active_connections)

        companies = 0
        branches = 0
        users = 0
        connections = 0

        for tenant in self.active_connections.values():

            companies += len(tenant)

            for company in tenant.values():

                branches += len(company)

                for branch in company.values():

                    users += len(branch)

                    for user in branch.values():

                        connections += len(user)

        return {
            "tenants": tenants,
            "companies": companies,
            "branches": branches,
            "users": users,
            "connections": connections,
        }

    async def heartbeat(
        self,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        user_id: str,
        connection_id: str,
    ):

        try:

            self.active_connections[
                tenant_id
            ][
                company_id
            ][
                branch_id
            ][
                user_id
            ][
                connection_id
            ]["last_ping"] = datetime.now(timezone.utc)

        except KeyError:
            pass

    # =================================================
    # GET CONNECTION
    # =================================================

    def get_connection(
        self,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        user_id: str,
        connection_id: str,
    ) -> ConnectionInfo | None:

        try:

            return self.active_connections[ tenant_id ][ company_id ][ branch_id ][ user_id ][ connection_id ]

        except KeyError:

            return None

    # =================================================
    # GET USER CONNECTIONS
    # =================================================

    def get_user_connections(
        self,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        user_id: str,
    ) -> dict[str, ConnectionInfo]:

        try:

            return self.active_connections[
                tenant_id
            ][
                company_id
            ][
                branch_id
            ][
                user_id
            ]

        except KeyError:

            return {}

    # =================================================
    # IS USER ONLINE
    # =================================================

    def is_online(
        self,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        user_id: str,
    ) -> bool:

        return bool(
            self.get_user_connections(
                tenant_id,
                company_id,
                branch_id,
                user_id,
            )
        )

    # =================================================
    # ONLINE USERS
    # =================================================

    def get_online_users(
        self,
        tenant_id: str,
        company_id: str,
        branch_id: str,
    ) -> list[str]:

        try:

            return list(
                self.active_connections[
                    tenant_id
                ][
                    company_id
                ][
                    branch_id
                ].keys()
            )

        except KeyError:

            return []

    # =================================================
    # ONLINE BRANCHES
    # =================================================

    def get_online_branches(
        self,
        tenant_id: str,
        company_id: str,
    ) -> list[str]:

        try:

            return list(
                self.active_connections[
                    tenant_id
                ][
                    company_id
                ].keys()
            )

        except KeyError:

            return []


    # =================================================
    # ONLINE COMPANIES
    # =================================================

    def get_online_companies(
        self,
        tenant_id: str,
    ) -> list[str]:

        try:

            return list(
                self.active_connections[
                    tenant_id
                ].keys()
            )

        except KeyError:

            return []

    # =================================================
    # ONLINE TENANTS
    # =================================================

    def get_online_tenants(
        self,
    ) -> list[str]:

        return list(
            self.active_connections.keys()
        )

    # =================================================
    # USER CONNECTION COUNT
    # =================================================

    def user_connection_count(
        self,
        tenant_id: str,
        company_id: str,
        branch_id: str,
        user_id: str,
    ) -> int:

        return len(
            self.get_user_connections(
                tenant_id,
                company_id,
                branch_id,
                user_id,
            )
        )

    # =================================================
    # ALL CONNECTIONS
    # =================================================

    def all_connections(
        self,
    ) -> list[ConnectionInfo]:

        connections = []

        for tenant in self.active_connections.values():

            for company in tenant.values():

                for branch in company.values():

                    for user in branch.values():

                        connections.extend(
                            user.values()
                        )

        return connections

    # =================================================
    # CONNECTIONS BY ROLE
    # =================================================

    def get_role_connections(
        self,
        tenant_id: str,
        company_id: str,
        role: str,
    ) -> list[ConnectionInfo]:

        results = []

        try:

            company = self.active_connections[
                tenant_id
            ][
                company_id
            ]

            for branch in company.values():

                for user in branch.values():

                    for connection in user.values():

                        if connection["role"] == role:

                            results.append(
                                connection
                            )

        except KeyError:

            pass

        return results


manager = ConnectionManager()