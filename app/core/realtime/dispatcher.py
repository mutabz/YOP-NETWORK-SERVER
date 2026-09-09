# app/core/realtime/dispatcher.py

from typing import Callable, Awaitable


RealtimeHandler = Callable[..., Awaitable]


class Dispatcher:

    """
    Realtime Event Dispatcher

    Responsibilities:
        - Receive incoming websocket events
        - Find matching handler
        - Execute handler

    It does NOT:
        - Know business logic
        - Know notifications
        - Know invoices
        - Know inventory

    Handlers are registered externally.
    """


    def __init__(self):

        self._handlers: dict[
            str,
            RealtimeHandler
        ] = {}


    # =====================================
    # REGISTER HANDLER
    # =====================================

    def register(
        self,
        event: str,
        handler: RealtimeHandler,
    ):
        """
        Register websocket event handler.

        Example:

        dispatcher.register(
            "notification.read",
            notification_read_handler
        )
        """

        self._handlers[event] = handler



    # =====================================
    # UNREGISTER HANDLER
    # =====================================

    def unregister(
        self,
        event: str,
    ):
        """
        Remove event handler.
        """

        self._handlers.pop(
            event,
            None
        )



    # =====================================
    # CHECK HANDLER
    # =====================================

    def has_handler(
        self,
        event: str,
    ) -> bool:

        return event in self._handlers



    # =====================================
    # LIST EVENTS
    # =====================================

    def registered_events(self):

        return list(
            self._handlers.keys()
        )



    # =====================================
    # DISPATCH EVENT
    # =====================================

    async def dispatch(
        self,
        *,
        user: dict,
        payload: dict,
    ):

        event = payload.get(
            "event"
        )

        data = payload.get(
            "data",
            {}
        )


        if not event:
            return


        handler = self._handlers.get(
            event
        )


        if not handler:

            print(
                f"⚠️ Unknown realtime event: {event}"
            )

            return



        await handler(
            user=user,
            data=data,
        )



dispatcher = Dispatcher()