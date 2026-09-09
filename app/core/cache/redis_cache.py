import json
import hashlib
import functools
from typing import Any, Callable, Optional

from sqlalchemy.inspection import inspect
from app.core.cache.redis_client import redis_client


# =========================================================
# 🔧 SERIALIZER (SQLAlchemy → JSON SAFE)
# =========================================================
def serialize(result: Any):
    if result is None:
        return None

    if isinstance(result, list):
        return [serialize(r) for r in result]

    # SQLAlchemy model
    if hasattr(result, "__table__"):
        return {
            c.key: getattr(result, c.key)
            for c in inspect(result).mapper.column_attrs
        }

    # dict safe
    if isinstance(result, dict):
        return result

    return result


# =========================================================
# 🔑 CACHE KEY BUILDER
# =========================================================
def build_cache_key(prefix, func_name, company_id, branch_id, args, kwargs):
    payload = {
        "func": func_name,
        "company_id": company_id,
        "branch_id": branch_id,
        "args": str(args),
        "kwargs": str(kwargs)
    }

    raw = json.dumps(payload, sort_keys=True, default=str)
    hashed = hashlib.md5(raw.encode()).hexdigest()

    return f"{prefix}:{hashed}"


# =========================================================
# 🏷 CACHE TAG BUILDER
# =========================================================
def build_tag(company_id, branch_id, model_name):
    return f"tag:{company_id}:{branch_id}:{model_name}"


# =========================================================
# ⚡ CACHE DECORATOR (ERP READY)
# =========================================================
def cached_query(
    ttl: int = 60,
    prefix: str = "sqlcache",
    model_name: str = "default"
):
    def decorator(func: Callable):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):

            if not redis_client:
                return await func(*args, **kwargs)

            company_id = kwargs.get("company_id", "global")
            branch_id = kwargs.get("branch_id", "global")

            # 🔑 cache key
            cache_key = build_cache_key(
                prefix,
                func.__name__,
                company_id,
                branch_id,
                args,
                kwargs
            )

            # 🚀 CHECK CACHE
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # ❌ DB CALL
            result = await func(*args, **kwargs)

            # 💾 STORE CACHE
            await redis_client.setex(
                cache_key,
                ttl,
                json.dumps(serialize(result), default=str)
            )

            # 🏷 TAG FOR INVALIDATION
            tag = build_tag(company_id, branch_id, model_name)
            await redis_client.sadd(tag, cache_key)

            return result

        return wrapper

    return decorator


# =========================================================
# 🧹 CACHE INVALIDATION (MODEL LEVEL)
# =========================================================
async def invalidate_model_cache(
    company_id: str,
    branch_id: str,
    model_name: str
):
    if not redis_client:
        return

    tag = build_tag(company_id, branch_id, model_name)

    keys = await redis_client.smembers(tag)

    if keys:
        await redis_client.delete(*keys)
        await redis_client.delete(tag)