from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi import WebSocketException

from app.core.realtime import manager
from app.core.realtime.auth import authenticate_websocket
from app.core.realtime.dispatcher import dispatcher


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):
    """
    =====================================================
    ERP WEBSOCKET GATEWAY
    =====================================================

    Responsibilities
    ----------------
    - Authenticate websocket
    - Accept connection
    - Register connection
    - Receive client messages
    - Dispatch incoming events
    - Cleanup on disconnect

    Keep this gateway thin.
    Business logic belongs in dispatcher handlers.
    """

    # =====================================
    # AUTHENTICATE
    # =====================================

    user = await authenticate_websocket(websocket)

    # =====================================
    # ACCEPT CONNECTION
    # =====================================

    await websocket.accept()

    # =====================================
    # REGISTER CONNECTION
    # =====================================

    connection_id = await manager.register(
        websocket=websocket,
        tenant_id=user["tenant_id"],
        company_id=user["company_id"],
        branch_id=user["branch_id"],
        user_id=user["user_id"],
        role=user["roles"][0] if user["roles"] else "user",
    )

    try:

        # =====================================
        # CONNECTION SUCCESS
        # =====================================

        await manager.send_to_user(
            tenant_id=user["tenant_id"],
            company_id=user["company_id"],
            branch_id=user["branch_id"],
            user_id=user["user_id"],
            message={
                "event": "system.connected",
                "data": {
                    "message": "Connected successfully"
                }
            },
        )

        # =====================================
        # RECEIVE LOOP
        # =====================================

        while True:

            payload = await websocket.receive_json()

            if payload.get("event") == "system.ping":

                await manager.heartbeat(
                    tenant_id=user["tenant_id"],
                    company_id=user["company_id"],
                    branch_id=user["branch_id"],
                    user_id=user["user_id"],
                    connection_id=connection_id,
                )

            await dispatcher.dispatch(
                user=user,
                payload=payload,
            )

    except WebSocketDisconnect:
        pass

    except WebSocketException:
        pass

    except Exception as e:
        print(f"Realtime Error: {e}")

    finally:

        await manager.unregister(
            tenant_id=user["tenant_id"],
            company_id=user["company_id"],
            branch_id=user["branch_id"],
            user_id=user["user_id"],
            connection_id=connection_id,
        )