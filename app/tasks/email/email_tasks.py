from app.core.celery_app import celery_app


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_email_task(self, tenant_id: str, email: str, subject: str, message: str):

    print(f"[EMAIL] tenant={tenant_id} -> {email}")

    # simulate email provider failure handling
    if not email:
        raise ValueError("Invalid email")

    return {
        "status": "sent",
        "tenant_id": tenant_id
    }