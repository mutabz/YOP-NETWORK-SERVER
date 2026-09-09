import asyncio

from app.core.celery_app import celery_app
from app.events.event_types import EventType
from app.shared.background.dispatcher import dispatch


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def publish_background_event(
    self,
    event_type: str,
    payload: dict,
):
    """
    Celery worker responsible for dispatching background events.
    """
    asyncio.run(
        dispatch(
            event_type=EventType(event_type),
            payload=payload,
        )
    )