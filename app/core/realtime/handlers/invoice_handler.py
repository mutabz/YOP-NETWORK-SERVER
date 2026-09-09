from app.core.realtime.publisher import publisher
from app.core.realtime.events import RealtimeEvent


async def invoice_created_realtime_handler(event):

    print("""
        Handles invoice.created events.
    
        Responsibilities:
            - Receive business event
            - Extract context
            - Push websocket messages
            - Target users by branch/role
        """)

    print(event)
    context = event.get( "context", {} )
    data = event.get( "data", {} )
    tenant_id = context.get( "tenant_id" )
    company_id = context.get( "company_id" )
    branch_id = context.get( "branch_id" )
    user_id = context.get( "user_id" )

    if not tenant_id or not branch_id:
        return


    message = {

        "event": "invoice.created",

        "data": {

            **data,

            "company_id": company_id,
            "branch_id": branch_id

        }

    }


    target_roles = data.get(
        "target_roles",
        []
    )


    # =====================================
    # SEND TO SPECIFIC ROLES
    # =====================================

    await publisher.to_branch(
        tenant_id=tenant_id,
        company_id=company_id,
        branch_id=branch_id,
        event=RealtimeEvent.INVOICE_CREATED,
        data=message["data"],
    )
