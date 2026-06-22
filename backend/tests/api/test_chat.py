import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_chat_unauthorized(client: AsyncClient):
    response = await client.post(
        "/api/v1/chat",
        json={"message": "Hello"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_chat(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/api/v1/chat",
        json={"message": "Find gaming laptops under 100000"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "session_id" in data
    assert "metadata" in data


@pytest.mark.asyncio
async def test_chat_with_context(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/api/v1/chat",
        json={
            "message": "Find phones",
            "context": {"budget": 50000, "category": "smartphones"},
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
