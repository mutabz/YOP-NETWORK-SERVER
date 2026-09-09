from app.shared.background.worker import publish_background_event
from app.events.event_types import EventType

class BackgroundManager:

    @staticmethod
    def publish(
        event_type: EventType,
        payload: dict,
    ):        

        """
        Queue a background event for asynchronous processing.
        """

        publish_background_event.delay(
            event_type=event_type.value,
            payload=payload,
        )

