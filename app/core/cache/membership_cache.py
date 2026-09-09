import json
from app.core.cache.redis_client import redis_client


class MembershipCache:

    @staticmethod
    async def get_memberships(user_id: str):
        key = f"user:{user_id}:memberships"
        data = await redis_client.get(key)

        if data:
            return json.loads(data)

        return None


    @staticmethod
    async def set_memberships(user_id: str, memberships: list, ttl: int = 1):
        key = f"user:{user_id}:memberships"

        await redis_client.set(
            key,
            json.dumps(memberships),
            ex=ttl
        )


    @staticmethod
    async def clear_memberships(user_id: str):
        key = f"user:{user_id}:memberships"
        await redis_client.delete(key)