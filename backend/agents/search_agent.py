from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import async_session_factory
from database.models import Product


async def search_products(state: dict[str, Any]) -> dict[str, Any]:
    intent = state.get("intent", {})

    async with async_session_factory() as db:
        query = select(Product).where(Product.availability == True)

        if intent.get("category"):
            query = query.where(Product.category == intent["category"])

        budget = intent.get("budget") or {}
        if budget.get("max"):
            query = query.where(Product.price <= budget["max"])

        if budget.get("min"):
            query = query.where(Product.price >= budget["min"])

        if intent.get("brands"):
            brand_list = [b.lower() for b in intent["brands"]]
            query = query.where(Product.brand.ilikeAny(brand_list))

        query = query.order_by(Product.rating.desc().nullslast()).limit(20)

        result = await db.execute(query)
        products = result.scalars().all()

        products_list = []
        for product in products:
            products_list.append({
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
            })

    return {
        "products": products_list,
        "metadata": {
            "products_found": len(products_list),
            "search_criteria": intent,
        },
    }
