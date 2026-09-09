from app.events.register import register_events


def init_celery_events():
    register_events()