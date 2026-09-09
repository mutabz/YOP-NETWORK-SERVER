from app.core.db_imports import *  # noqa
from celery import Celery
from kombu import Exchange, Queue

from app.core.config import settings
from celery.signals import worker_process_init



celery_app = Celery(
    "erp_system",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.shared.background.worker",
    ]
)


@worker_process_init.connect
def init_worker(**kwargs):

    from app.events.register import register_events

    register_events()
    
# =====================================================
# QUEUES
# =====================================================

default_exchange = Exchange(
    "erp",
    type="direct"
)

celery_app.conf.task_queues = (
    Queue(
        "critical",
        default_exchange,
        routing_key="critical"
    ),

    Queue(
        "high_priority",
        default_exchange,
        routing_key="high_priority"
    ),

    Queue(
        "medium_priority",
        default_exchange,
        routing_key="medium_priority"
    ),

    Queue(
        "low_priority",
        default_exchange,
        routing_key="low_priority"
    ),

    Queue(
        "dead_letter",
        default_exchange,
        routing_key="dead_letter"
    ),
)

# =====================================================
# ROUTING
# =====================================================

celery_app.conf.task_routes = {
}

# =====================================================
# SERIALIZATION
# =====================================================

celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]

# =====================================================
# TIMEZONE
# =====================================================

celery_app.conf.timezone = "Africa/Kigali"
celery_app.conf.enable_utc = True

# =====================================================
# RELIABILITY
# =====================================================

celery_app.conf.task_acks_late = True
celery_app.conf.task_reject_on_worker_lost = True

celery_app.conf.worker_prefetch_multiplier = 1

celery_app.conf.broker_connection_retry_on_startup = True

# =====================================================
# RATE LIMITS
# =====================================================

celery_app.conf.task_annotations = {
    "*": {
        "rate_limit": "200/s"
    }
}

# =====================================================
# RESULT STORAGE
# =====================================================

celery_app.conf.result_expires = 86400

celery_app.conf.task_track_started = True

celery_app.conf.result_extended = True

# =====================================================
# TIME LIMITS
# =====================================================

celery_app.conf.task_soft_time_limit = 300

celery_app.conf.task_time_limit = 600

# =====================================================
# EVENTS
# =====================================================

celery_app.conf.worker_send_task_events = True

celery_app.conf.task_send_sent_event = True

# =====================================================
# BEAT
# =====================================================

celery_app.conf.beat_schedule = {

    "cleanup-expired-cache": {
        "task": "app.tasks.audit_tasks.cleanup_cache",
        "schedule": 3600,
    },

    "daily-reports": {
        "task": "app.tasks.report_tasks.generate_daily_reports",
        "schedule": 86400,
    },
}

# =====================================================
# DEFAULTS
# =====================================================

celery_app.conf.task_default_queue = "medium_priority"

celery_app.conf.task_default_exchange = "erp"

celery_app.conf.task_default_routing_key = "medium_priority"