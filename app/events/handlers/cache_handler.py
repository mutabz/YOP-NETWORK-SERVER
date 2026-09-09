from app.core.cache.invalidation import (
    invalidate_model_cache,
    invalidate_multiple_models
)


async def cache_handler(payload):

    models = payload.get("models")

    if models:

        await invalidate_multiple_models(
            payload["company_id"],
            payload["branch_id"],
            models
        )

        return

    await invalidate_model_cache(
        payload["company_id"],
        payload["branch_id"],
        payload["model"]
    )