# app/core/realtime/registry.py

from app.core.realtime.dispatcher import dispatcher

from app.core.realtime.events import RealtimeEvent

from app.core.realtime.handlers.system import ping



def register_realtime_handlers():

    dispatcher.register(
        RealtimeEvent.PING.value,
        ping,
    )


    print(
        "✅ Realtime handlers registered"
    )