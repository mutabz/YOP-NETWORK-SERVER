from app.core.cache.redis_client import redis_client


async def invalidate_model_cache(
    company_id,
    branch_id,
    model_name
):

    tag = f"tag:{company_id}:{branch_id}:{model_name}"

    keys = await redis_client.smembers(tag)

    if keys:

        await redis_client.delete(*keys)

        await redis_client.delete(tag)


async def invalidate_multiple_models(
    company_id,
    branch_id,
    models: list[str]
):

    for model in models:

        await invalidate_model_cache(
            company_id,
            branch_id,
            model
        )