import uuid

import pytest
from httpx import AsyncClient

from database.models import Product
from database.connection import async_session_factory


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    response = await client.get(f"/api/v1/products/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_recommend_products(client: AsyncClient, auth_headers: dict):
    async with async_session_factory() as db:
        product = Product(
            title="Test Laptop",
            price=89990,
            category="laptops",
            brand="TestBrand",
            rating=4.5,
        )
        db.add(product)
        await db.commit()

    response = await client.post(
        "/api/v1/products/recommend",
        json={"category": "laptops", "limit": 5},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "categories" in data


@pytest.mark.asyncio
async def test_compare_products(client: AsyncClient):
    async with async_session_factory() as db:
        product1 = Product(
            title="Product 1",
            price=50000,
            category="laptops",
            brand="Brand1",
            rating=4.3,
        )
        product2 = Product(
            title="Product 2",
            price=60000,
            category="laptops",
            brand="Brand2",
            rating=4.5,
        )
        db.add_all([product1, product2])
        await db.commit()
        await db.refresh(product1)
        await db.refresh(product2)

        product_ids = [str(product1.id), str(product2.id)]

    response = await client.post(
        "/api/v1/products/compare",
        json={"product_ids": product_ids},
    )
    assert response.status_code == 200
    data = response.json()
    assert "comparison" in data
