from app.events.event_types import EventType
from app.shared.managers.workflow_manager import WorkflowManager


async def dispatch(
    event_type: EventType,
    payload: dict,
):
    """
    Dispatch a background event into the workflow system.
    """
    await WorkflowManager.publish(
        event_type=event_type,
        payload=payload,
    )