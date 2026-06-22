import uuid
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import async_session_factory
from database.models import PriceHistory, PriceTracking, Product
from mcp_servers.base import MCPServer

pricing_server = MCPServer("pricing")


@pricing_server.tool(
    name="track_price",
    description="Start tracking a product's price",
)
async def track_price(
    user_id: str,
    product_id: str,
    target_price: float,
    alert_on_drop: bool = True,
) -> dict[str, Any]:
    async with async_session_factory() as db:
        stmt = select(Product).where(Product.id == uuid.UUID(product_id))
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            return {"error": "Product not found"}

        tracking = PriceTracking(
            user_id=uuid.UUID(user_id),
            product_id=uuid.UUID(product_id),
            target_price=target_price,
            alert_on_drop=alert_on_drop,
        )
        db.add(tracking)
        await db.commit()
        await db.refresh(tracking)

        return {
            "tracking_id": str(tracking.id),
            "product_id": product_id,
            "target_price": target_price,
            "current_price": product.price,
            "status": "active",
        }


@pricing_server.tool(
    name="get_price_history",
    description="Get price history for a product",
)
async def get_price_history(
    product_id: str,
    period: str = "30d",
) -> dict[str, Any]:
    async with async_session_factory() as db:
        period_days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}
        start_date = datetime.utcnow() - timedelta(days=period_days.get(period, 30))

        stmt = (
            select(PriceHistory)
            .where(PriceHistory.product_id == uuid.UUID(product_id))
            .where(PriceHistory.recorded_at >= start_date)
            .order_by(PriceHistory.recorded_at)
        )

        result = await db.execute(stmt)
        history = result.scalars().all()

        if not history:
            return {
                "history": [],
                "statistics": {},
            }

        prices = [h.price for h in history]

        return {
            "history": [
                {
                    "price": h.price,
                    "source": h.source,
                    "recorded_at": h.recorded_at.isoformat(),
                }
                for h in history
            ],
            "statistics": {
                "lowest": min(prices),
                "highest": max(prices),
                "average": round(sum(prices) / len(prices), 2),
                "current": prices[-1] if prices else 0,
                "data_points": len(prices),
            },
        }


@pricing_server.tool(
    name="predict_price_drop",
    description="Predict if a product price will drop soon",
)
async def predict_price_drop(product_id: str) -> dict[str, Any]:
    async with async_session_factory() as db:
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        stmt = (
            select(PriceHistory)
            .where(PriceHistory.product_id == uuid.UUID(product_id))
            .where(PriceHistory.recorded_at >= thirty_days_ago)
            .order_by(PriceHistory.recorded_at)
        )

        result = await db.execute(stmt)
        history = result.scalars().all()

        if len(history) < 2:
            return {
                "will_drop": False,
                "confidence": 0.3,
                "reasoning": "Insufficient price history data",
            }

        prices = [h.price for h in history]
        recent_avg = sum(prices[-3:]) / len(prices[-3:])
        older_avg = sum(prices[:3]) / len(prices[:3]) if len(prices) >= 3 else prices[0]

        change_pct = ((recent_avg - older_avg) / older_avg) * 100

        if change_pct < -5:
            return {
                "will_drop": True,
                "confidence": 0.75,
                "predicted_price": round(recent_avg * 0.95, 2),
                "reasoning": "Price has been trending downwards",
                "best_time": "Wait 1-2 weeks for potential further drops",
            }
        elif change_pct > 5:
            return {
                "will_drop": False,
                "confidence": 0.6,
                "reasoning": "Price is currently increasing",
                "best_time": "Buy now before prices increase further",
            }
        else:
            return {
                "will_drop": False,
                "confidence": 0.5,
                "reasoning": "Price is relatively stable",
                "best_time": "Current price is fair, buy when needed",
            }
