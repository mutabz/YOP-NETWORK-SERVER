from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

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
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.modules.system_layer.licensing.subscription.models import License
from app.modules.system_layer.organisation.repositories.company_membership import CompanyMembershipRepository


class RequestContextMiddleware(BaseHTTPMiddleware):

    EXCLUDED_PATHS = {
        "/api/v1/auth/login",
        "/api/v1/auth/refresh",
        "/api/v1/auth/register",
        "/api/v1/auth/contexts",
        "/api/v1/auth/forgot-password",
        "/api/v1/auth/reset-password",
        "/api/v1/non-auth/licensing/plans",
        "/docs",
        "/openapi.json",
    }


    async def dispatch(self, request: Request, call_next):

        # Skip JWT validation for public/auth endpoints
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)


        identity_token = current_identity.set(None)
        user_token = current_user_id.set(None)
        tenant_token = current_tenant_id.set(None)
        company_token = current_company_id.set(None)
        branch_token = current_branch_id.set(None)


        try:

            auth = request.headers.get("Authorization")


            if auth and auth.startswith("Bearer "):

                jwt_token = auth.removeprefix("Bearer ").strip()

                payload = decode_token(jwt_token)
                try:
                    async with AsyncSessionLocal() as session:

                        membership_id = payload.get("membership_id")
                        membership_repo = CompanyMembershipRepository(session)

                        role_names = await membership_repo.get_role_names(membership_id)

                        permission_codes = await membership_repo.get_permission_codes(
                            membership_id
                        )
                except Exception as e:
                    print("==="*50)

                # Invalid or expired JWT
                if not payload:
                    return JSONResponse(
                        status_code=401,
                        content={
                            "message": "Invalid or expired token"
                        }
                    )


                token_type = payload.get("type")

                # Prevent refresh tokens or unknown token types being used as access tokens
                if token_type not in {"identity", "context"}:
                    return JSONResponse(
                        status_code=401,
                        content={
                            "message": "Access token required"
                        }
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


                current_identity.set(identity)

                current_user_id.set(identity.user_id)
                current_tenant_id.set(identity.tenant_id)
                current_company_id.set(identity.company_id)
                current_branch_id.set(identity.branch_id)

                request.state.identity = identity

                if self._should_verify_license(request):
                    license_ok = await self._verify_license(identity, request)
                    if not license_ok:
                        return JSONResponse(status_code=403, content={"message": "License verification failed"})

            response = await call_next(request)

            return response



        finally:

            current_identity.reset(identity_token)
            current_user_id.reset(user_token)
            current_tenant_id.reset(tenant_token)
            current_company_id.reset(company_token)
            current_branch_id.reset(branch_token)

    def _should_verify_license(self, request: Request) -> bool:
        path = request.url.path
        return path.startswith("/api/companies/platform") or path.startswith("/api/v2") or path.startswith("/api/users/platform") or path.startswith("/api/tenants/platform")

    async def _verify_license(self, identity, request: Request) -> bool:
        company_id = identity.company_id or getattr(request.state, "company_id", None)
        print(company_id)
        print(identity)
        if not company_id:
            return False

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(License).where(
                    License.company_id == company_id,
                    License.status == "ACTIVE",
                    License.revoked.is_(False),
                )
            )
            license = result.scalars().first()
            print(result.mappings())
            return license is not None