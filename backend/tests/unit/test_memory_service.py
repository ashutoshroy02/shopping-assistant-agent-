import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestMemoryService:
    def test_add_message(self):
        mock_redis = MagicMock()
        mock_redis.rpush = AsyncMock()
        mock_redis.expire = AsyncMock()

        with patch("services.memory.redis.from_url", return_value=mock_redis):
            from services.memory import MemoryService
            memory = MemoryService.__new__(MemoryService)
            memory.redis = mock_redis
            memory.default_ttl = MagicMock(total_seconds=MagicMock(return_value=86400))

            import asyncio
            asyncio.run(memory.add_message("session123", "user", "Hello world"))

            mock_redis.rpush.assert_called_once()

    def test_get_conversation_history(self):
        mock_redis = MagicMock()
        mock_redis.lrange = AsyncMock(return_value=[
            json.dumps({"role": "user", "content": "Hello"}),
            json.dumps({"role": "assistant", "content": "Hi there!"}),
        ])

        with patch("services.memory.redis.from_url", return_value=mock_redis):
            from services.memory import MemoryService
            memory = MemoryService.__new__(MemoryService)
            memory.redis = mock_redis

            import asyncio
            history = asyncio.run(memory.get_conversation_history("session123"))

            assert len(history) == 2
            assert history[0]["role"] == "user"

    def test_update_user_preferences(self):
        mock_redis = MagicMock()
        mock_redis.get = AsyncMock(return_value=json.dumps({"categories": ["laptops"]}))
        mock_redis.set = AsyncMock()

        with patch("services.memory.redis.from_url", return_value=mock_redis):
            from services.memory import MemoryService
            memory = MemoryService.__new__(MemoryService)
            memory.redis = mock_redis
            memory.default_ttl = MagicMock(total_seconds=MagicMock(return_value=86400))

            import asyncio
            asyncio.run(memory.update_user_preferences("user123", {"budget": 50000}))

            mock_redis.set.assert_called_once()

    def test_add_saved_product(self):
        mock_redis = MagicMock()
        mock_redis.sadd = AsyncMock()
        mock_redis.expire = AsyncMock()

        with patch("services.memory.redis.from_url", return_value=mock_redis):
            from services.memory import MemoryService
            memory = MemoryService.__new__(MemoryService)
            memory.redis = mock_redis
            memory.default_ttl = MagicMock(total_seconds=MagicMock(return_value=86400))

            import asyncio
            asyncio.run(memory.add_saved_product("user123", "product456"))

            mock_redis.sadd.assert_called_once()

    def test_get_saved_products(self):
        mock_redis = MagicMock()
        mock_redis.smembers = AsyncMock(return_value=["product1", "product2"])

        with patch("services.memory.redis.from_url", return_value=mock_redis):
            from services.memory import MemoryService
            memory = MemoryService.__new__(MemoryService)
            memory.redis = mock_redis

            import asyncio
            saved = asyncio.run(memory.get_saved_products("user123"))

            assert len(saved) == 2
