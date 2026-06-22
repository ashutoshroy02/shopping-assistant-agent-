import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import async_session_factory
from database.models import Product
from mcp_servers.base import MCPServer

product_server = MCPServer("product")


@product_server.tool(
    name="search_products",
    description="Search for products with filters",
)
async def search_products(
    query: str = "",
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    brands: list[str] | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    async with async_session_factory() as db:
        stmt = select(Product).where(Product.availability == True)

        if category:
            stmt = stmt.where(Product.category == category)

        if min_price is not None:
            stmt = stmt.where(Product.price >= min_price)

        if max_price is not None:
            stmt = stmt.where(Product.price <= max_price)

        if brands:
            stmt = stmt.where(Product.brand.ilikeAny([f"%{b}%" for b in brands]))

        if query:
            stmt = stmt.where(
                Product.title.ilike(f"%{query}%")
                | Product.description.ilike(f"%{query}%")
            )

        stmt = stmt.order_by(Product.rating.desc().nullslast()).limit(limit)

        result = await db.execute(stmt)
        products = result.scalars().all()

        return {
            "products": [
                {
                    "id": str(p.id),
                    "title": p.title,
                    "price": p.price,
                    "rating": p.rating,
                    "category": p.category,
                    "brand": p.brand,
                }
                for p in products
            ],
            "total": len(products),
        }


@product_server.tool(
    name="get_product_details",
    description="Get detailed information about a specific product",
)
async def get_product_details(product_id: str) -> dict[str, Any]:
    async with async_session_factory() as db:
        stmt = select(Product).where(Product.id == uuid.UUID(product_id))
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            return {"error": "Product not found"}

        return {
            "id": str(product.id),
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "original_price": product.original_price,
            "rating": product.rating,
            "review_count": product.review_count,
            "category": product.category,
            "brand": product.brand,
            "specifications": product.specifications,
            "images": product.images,
            "availability": product.availability,
        }


@product_server.tool(
    name="compare_products",
    description="Compare multiple products side by side",
)
async def compare_products(product_ids: list[str]) -> dict[str, Any]:
    async with async_session_factory() as db:
        uuid_ids = [uuid.UUID(pid) for pid in product_ids]
        stmt = select(Product).where(Product.id.in_(uuid_ids))
        result = await db.execute(stmt)
        products = result.scalars().all()

        if len(products) < 2:
            return {"error": "At least 2 products required for comparison"}

        comparison = []
        for p in products:
            comparison.append({
                "id": str(p.id),
                "title": p.title,
                "price": p.price,
                "rating": p.rating,
                "specifications": p.specifications,
            })

        return {"comparison": comparison}


@product_server.tool(
    name="recommend_products",
    description="Get product recommendations based on criteria",
)
async def recommend_products(
    category: str,
    budget: float | None = None,
    use_case: str | None = None,
    limit: int = 5,
) -> dict[str, Any]:
    async with async_session_factory() as db:
        stmt = select(Product).where(
            Product.category == category,
            Product.availability == True,
        )

        if budget:
            stmt = stmt.where(Product.price <= budget)

        stmt = stmt.order_by(Product.rating.desc().nullslast()).limit(limit)

        result = await db.execute(stmt)
        products = result.scalars().all()

        recommendations = []
        for p in products:
            score = (p.rating or 0) / 5.0
            recommendations.append({
                "id": str(p.id),
                "title": p.title,
                "price": p.price,
                "rating": p.rating,
                "score": round(score, 2),
                "reasoning": f"Recommended based on {category} category",
            })

        return {"recommendations": recommendations}
