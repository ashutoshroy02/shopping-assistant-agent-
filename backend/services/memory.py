import json
from collections import defaultdict
from datetime import timedelta
from typing import Any

from config import get_settings

settings = get_settings()


class InMemoryStore:
    def __init__(self):
        self.lists: dict[str, list[str]] = defaultdict(list)
        self.strings: dict[str, str] = {}
        self.sets: dict[str, set[str]] = defaultdict(set)
        self.counters: dict[str, int] = defaultdict(int)

    async def rpush(self, key: str, value: str):
        self.lists[key].append(value)

    async def lrange(self, key: str, start: int, end: int) -> list[str]:
        data = self.lists[key]
        if end == -1:
            return data[start:]
        return data[start : end + 1]

    async def ltrim(self, key: str, start: int, end: int):
        self.lists[key] = self.lists[key][start : end + 1]

    async def lpush(self, key: str, value: str):
        self.lists[key].insert(0, value)

    async def get(self, key: str) -> str | None:
        return self.strings.get(key)

    async def set(self, key: str, value: str, ex: int | None = None):
        self.strings[key] = value

    async def expire(self, key: str, seconds: int):
        pass

    async def sadd(self, key: str, value: str):
        self.sets[key].add(value)

    async def srem(self, key: str, value: str):
        self.sets[key].discard(value)

    async def smembers(self, key: str) -> set[str]:
        return self.sets[key]

    async def sismember(self, key: str, value: str) -> bool:
        return value in self.sets[key]

    async def incr(self, key: str) -> int:
        self.counters[key] += 1
        return self.counters[key]


class MemoryService:
    def __init__(self):
        try:
            import redis.asyncio as redis
            self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
            self._use_redis = True
        except Exception:
            self.redis = InMemoryStore()
            self._use_redis = False
        self.default_ttl = timedelta(days=30)

    async def get_conversation_history(
        self, session_id: str, limit: int = 50
    ) -> list[dict[str, Any]]:
        key = f"chat:history:{session_id}"
        messages = await self.redis.lrange(key, -limit, -1)
        return [json.loads(msg) for msg in messages]

    async def add_message(
        self, session_id: str, role: str, content: str, metadata: dict | None = None
    ) -> None:
        key = f"chat:history:{session_id}"
        message = {
            "role": role,
            "content": content,
            "metadata": metadata or {},
        }
        await self.redis.rpush(key, json.dumps(message))
        await self.redis.expire(key, int(self.default_ttl.total_seconds()))

    async def get_user_preferences(self, user_id: str) -> dict[str, Any]:
        key = f"user:preferences:{user_id}"
        prefs = await self.redis.get(key)
        return json.loads(prefs) if prefs else {}

    async def update_user_preferences(
        self, user_id: str, preferences: dict[str, Any]
    ) -> None:
        key = f"user:preferences:{user_id}"
        current = await self.get_user_preferences(user_id)
        current.update(preferences)
        await self.redis.set(
            key, json.dumps(current), ex=int(self.default_ttl.total_seconds())
        )

    async def add_search_history(
        self, user_id: str, query: str, filters: dict | None = None
    ) -> None:
        key = f"user:searches:{user_id}"
        search = {
            "query": query,
            "filters": filters or {},
        }
        await self.redis.lpush(key, json.dumps(search))
        await self.redis.ltrim(key, 0, 99)
        await self.redis.expire(key, int(self.default_ttl.total_seconds()))

    async def get_search_history(
        self, user_id: str, limit: int = 20
    ) -> list[dict[str, Any]]:
        key = f"user:searches:{user_id}"
        searches = await self.redis.lrange(key, 0, limit - 1)
        return [json.loads(s) for s in searches]

    async def add_saved_product(self, user_id: str, product_id: str) -> None:
        key = f"user:saved:{user_id}"
        await self.redis.sadd(key, product_id)
        await self.redis.expire(key, int(self.default_ttl.total_seconds()))

    async def remove_saved_product(self, user_id: str, product_id: str) -> None:
        key = f"user:saved:{user_id}"
        await self.redis.srem(key, product_id)

    async def get_saved_products(self, user_id: str) -> list[str]:
        key = f"user:saved:{user_id}"
        return list(await self.redis.smembers(key))

    async def is_product_saved(self, user_id: str, product_id: str) -> bool:
        key = f"user:saved:{user_id}"
        return await self.redis.sismember(key, product_id)

    async def set_session_context(
        self, session_id: str, context: dict[str, Any]
    ) -> None:
        key = f"session:context:{session_id}"
        await self.redis.set(
            key, json.dumps(context), ex=int(timedelta(hours=2).total_seconds())
        )

    async def get_session_context(self, session_id: str) -> dict[str, Any]:
        key = f"session:context:{session_id}"
        context = await self.redis.get(key)
        return json.loads(context) if context else {}

    async def increment_user_activity(self, user_id: str, activity_type: str) -> int:
        key = f"user:activity:{user_id}:{activity_type}"
        count = await self.redis.incr(key)
        await self.redis.expire(key, int(timedelta(days=30).total_seconds()))
        return count

    async def get_user_activity(
        self, user_id: str, activity_type: str
    ) -> int:
        key = f"user:activity:{user_id}:{activity_type}"
        count = await self.redis.get(key)
        return int(count) if count else 0


memory_service = MemoryService()
