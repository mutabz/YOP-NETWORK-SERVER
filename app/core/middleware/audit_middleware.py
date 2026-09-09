from starlette.middleware.base import BaseHTTPMiddleware
from app.core.context.request_context import (
    current_user_id,
    current_tenant_id,
    current_company_id,
    current_branch_id
)


class AuditMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        # 👉 Extract from headers or JWT (adapt to your auth system)
        user_id = request.headers.get("x-user-id")
        tenant_id = request.headers.get("x-tenant-id")
        company_id = request.headers.get("x-company-id")
        branch_id = request.headers.get("x-branch-id")

        # Set context
        if user_id:
            current_user_id.set(user_id)
        if tenant_id:
            current_tenant_id.set(tenant_id)
        if company_id:
            current_company_id.set(company_id)
        if branch_id:
            current_branch_id.set(branch_id)

        response = await call_next(request)
        return response