import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import async_session_factory
from database.models import Product
from mcp_servers.base import MCPServer

deals_server = MCPServer("deals")


@deals_server.tool(
    name="find_discounts",
    description="Find current discounts for a product",
)
async def find_discounts(product_id: str) -> dict[str, Any]:
    async with async_session_factory() as db:
        stmt = select(Product).where(Product.id == uuid.UUID(product_id))
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            return {"error": "Product not found"}

        discounts = []

        if product.original_price and product.original_price > product.price:
            savings = product.original_price - product.price
            discount_pct = (savings / product.original_price) * 100

            discounts.append({
                "type": "price_drop",
                "original_price": product.original_price,
                "current_price": product.price,
                "savings": savings,
                "discount_percentage": round(discount_pct, 1),
                "description": f"Save ₹{savings:,.0f} ({discount_pct:.0f}% off)",
            })

        brand = product.brand.lower()
        brand_discounts = {
            "apple": {"code": "APPLE10", "discount": "10%"},
            "samsung": {"code": "SAMSUNG15", "discount": "15%"},
            "asus": {"code": "ASUS10", "discount": "10%"},
            "lenovo": {"code": "LENOVO12", "discount": "12%"},
        }

        if brand in brand_discounts:
            bd = brand_discounts[brand]
            discounts.append({
                "type": "coupon",
                "code": bd["code"],
                "discount": bd["discount"],
                "description": f"Use code {bd['code']} for {bd['discount']} off",
            })

        return {
            "product_id": product_id,
            "discounts": discounts,
            "total_discounts": len(discounts),
        }


@deals_server.tool(
    name="find_coupons",
    description="Find available coupons for a product or brand",
)
async def find_coupons(product_id: str) -> dict[str, Any]:
    async with async_session_factory() as db:
        stmt = select(Product).where(Product.id == uuid.UUID(product_id))
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            return {"error": "Product not found"}

        coupons = []
        brand = product.brand.lower()

        brand_coupons = {
            "apple": [
                {"code": "APPLE10", "discount": "10%", "min_purchase": 50000},
                {"code": "IPHONE5", "discount": "5%", "min_purchase": 30000},
            ],
            "samsung": [
                {"code": "SAMSUNG15", "discount": "15%", "min_purchase": 40000},
                {"code": "GALAXY10", "discount": "10%", "min_purchase": 20000},
            ],
            "asus": [
                {"code": "ASUS10", "discount": "10%", "min_purchase": 50000},
            ],
            "lenovo": [
                {"code": "LENOVO12", "discount": "12%", "min_purchase": 40000},
            ],
        }

        if brand in brand_coupons:
            for coupon in brand_coupons[brand]:
                if product.price >= coupon["min_purchase"]:
                    coupons.append({
                        "code": coupon["code"],
                        "discount": coupon["discount"],
                        "min_purchase": coupon["min_purchase"],
                        "valid": True,
                    })

        return {
            "product_id": product_id,
            "coupons": coupons,
            "total_coupons": len(coupons),
        }


@deals_server.tool(
    name="get_cashback_offers",
    description="Get cashback offers for a product",
)
async def get_cashback_offers(product_id: str) -> dict[str, Any]:
    async with async_session_factory() as db:
        stmt = select(Product).where(Product.id == uuid.UUID(product_id))
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            return {"error": "Product not found"}

        offers = []

        if product.price > 100000:
            cashback_pct = 5
        elif product.price > 50000:
            cashback_pct = 3
        elif product.price > 20000:
            cashback_pct = 2
        else:
            cashback_pct = 1

        cashback_amount = product.price * cashback_pct / 100

        offers.append({
            "type": "standard_cashback",
            "cashback_percentage": cashback_pct,
            "cashback_amount": round(cashback_amount, 2),
            "description": f"{cashback_pct}% cashback (₹{cashback_amount:,.0f})",
        })

        if product.price > 75000:
            offers.append({
                "type": "bonus_cashback",
                "cashback_percentage": 2,
                "cashback_amount": round(product.price * 0.02, 2),
                "description": "Additional 2% bonus cashback on orders above ₹75,000",
            })

        return {
            "product_id": product_id,
            "offers": offers,
            "total_offers": len(offers),
            "max_cashback": round(
                sum(o["cashback_amount"] for o in offers), 2
            ),
        }
