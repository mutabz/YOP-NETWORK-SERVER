from app.core.celery_app import celery_app


class BaseTask:
    """
    ERP task base with retry + logging support
    """

    @staticmethod
    def retry_task(task_func, *args, retries=3, countdown=5, **kwargs):
        try:
            return task_func(*args, **kwargs)
        except Exception as e:
            raise task_func.retry(
                exc=e,
                countdown=countdown,
                max_retries=retries
            )