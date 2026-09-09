from fastapi import WebSocket
from fastapi import WebSocketException, status

from app.core.auth.jwt import decode_token
from app.core.context.request_context import (
    IdentityContext,
    current_identity,
    current_user_id,
    current_tenant_id,
    current_company_id,
    current_branch_id,
)
from fastapi.responses import JSONResponse
import traceback
from app.core.database import AsyncSessionLocal

from app.modules.system_layer.organisation.repositories.company_membership import CompanyMembershipRepository


async def authenticate_websocket(
    websocket: WebSocket,
):
    """
    Authenticate a websocket connection.

    Only CONTEXT tokens are accepted.
    """

    # =====================================
    # TOKEN
    # =====================================

    token = websocket.query_params.get("token")

    if not token:

        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Authentication token required",
        )


    # =====================================
    # DECODE
    # =====================================

    payload = decode_token(token)
    

    if not payload:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Invalid or expired token",
        )
        
    # =====================================
    # TOKEN TYPE
    # =====================================

    if payload.get("type") != "context":

        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Context token required",
        )

    try:
        async with AsyncSessionLocal() as session:
            membership_id = payload.get("membership_id")
            membership_repo = CompanyMembershipRepository(session)

            role_names = await membership_repo.get_role_names(membership_id)

            permission_codes = await membership_repo.get_permission_codes(membership_id)

    except Exception:
        traceback.print_exc()
        raise

    # Invalid or expired JWT
    if not payload:
        print("Invalid or expired token")

    token_type = payload["type"]

    # Prevent refresh tokens or unknown token types being used as access tokens
    if token_type not in {"identity", "context"}:
        print(
                "Access token required"
        )

    identity = IdentityContext(
        user_id=payload.get("sub"),

        token_type=token_type,
        tenant_id=payload.get("tenant_id"),
        company_id=payload.get("company_id"),
        branch_id=payload.get("branch_id"),
        roles=role_names,
        permissions=permission_codes,
        scopes=payload.get("scopes", []),
        membership_id=membership_id,
        membership_type=payload.get("membership_type"),
        session_id=payload.get("session_id"),
        device_id=payload.get("device_id"),
        jti=payload.get("jti"),
    )




    # =====================================
    # REQUIRED CLAIMS
    # =====================================

    required = (
        "sub",
        "tenant_id",
        "company_id",
        "branch_id",
    )

    for key in required:

        if not payload.get(key):

            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason=f"Missing '{key}' claim",
            )

    # =====================================
    # IDENTITY
    # =====================================

    data = {
        "id": identity.user_id,
        "user_id": identity.user_id,
        "membership_id": identity.membership_id,
        "tenant_id": identity.tenant_id,
        "company_id": identity.company_id,
        "branch_id": identity.branch_id,
        "roles": identity.roles,
        "permissions": identity.permissions,
        "membership_type": identity.membership_type
    }
    return data