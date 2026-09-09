from app.events.register import register_events


_events_loaded = False


def load_events():

    global _events_loaded

    if _events_loaded:
        return

    register_events()

    _events_loaded = True