from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import async_session_factory
from database.models import PriceHistory


async def analyze_prices(state: dict[str, Any]) -> dict[str, Any]:
    products = state.get("products", [])

    price_insights = {}

    async with async_session_factory() as db:
        for product in products[:5]:
            product_id = product.get("id")

            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            query = (
                select(PriceHistory)
                .where(PriceHistory.product_id == product_id)
                .where(PriceHistory.recorded_at >= thirty_days_ago)
                .order_by(PriceHistory.recorded_at)
            )

            result = await db.execute(query)
            history = result.scalars().all()

            if history:
                prices = [h.price for h in history]
                price_insights[product_id] = {
                    "product_title": product.get("title"),
                    "current_price": product.get("price"),
                    "lowest_price": min(prices),
                    "highest_price": max(prices),
                    "average_price": round(sum(prices) / len(prices), 2),
                    "price_trend": calculate_price_trend(prices),
                    "volatility": calculate_volatility(prices),
                    "history": [
                        {
                            "price": h.price,
                            "source": h.source,
                            "date": h.recorded_at.isoformat(),
                        }
                        for h in history
                    ],
                }
            else:
                price_insights[product_id] = {
                    "product_title": product.get("title"),
                    "current_price": product.get("price"),
                    "lowest_price": product.get("price"),
                    "highest_price": product.get("price"),
                    "average_price": product.get("price"),
                    "price_trend": "stable",
                    "volatility": 0,
                    "history": [],
                }

    return {
        "price_insights": price_insights,
        "metadata": {
            "products_analyzed": len(price_insights),
        },
    }


def calculate_price_trend(prices: list[float]) -> str:
    if len(prices) < 2:
        return "stable"

    recent_avg = sum(prices[-3:]) / len(prices[-3:])
    older_avg = sum(prices[:3]) / len(prices[:3]) if len(prices) >= 3 else prices[0]

    change_pct = ((recent_avg - older_avg) / older_avg) * 100

    if change_pct < -5:
        return "decreasing"
    elif change_pct > 5:
        return "increasing"
    else:
        return "stable"


def calculate_volatility(prices: list[float]) -> float:
    if len(prices) < 2:
        return 0.0

    avg = sum(prices) / len(prices)
    variance = sum((p - avg) ** 2 for p in prices) / len(prices)
    std_dev = variance ** 0.5

    return round((std_dev / avg) * 100, 2)


async def predict_price_drop(state: dict[str, Any]) -> dict[str, Any]:
    products = state.get("products", [])
    price_insights = state.get("price_insights", {})

    predictions = {}

    for product in products[:5]:
        product_id = product.get("id")
        insights = price_insights.get(product_id, {})

        trend = insights.get("price_trend", "stable")
        current_price = product.get("price", 0)
        lowest_price = insights.get("lowest_price", current_price)

        prediction = generate_prediction(trend, current_price, lowest_price)
        predictions[product_id] = {
            "product_title": product.get("title"),
            "current_price": current_price,
            "predicted_drop": prediction["will_drop"],
            "predicted_price": prediction["predicted_price"],
            "confidence": prediction["confidence"],
            "best_time_to_buy": prediction["best_time"],
            "reasoning": prediction["reasoning"],
        }

    return {
        "predictions": predictions,
    }


def generate_prediction(
    trend: str, current_price: float, lowest_price: float
) -> dict[str, Any]:
    if trend == "decreasing":
        predicted_price = current_price * 0.92
        return {
            "will_drop": True,
            "predicted_price": round(predicted_price, 2),
            "confidence": 0.75,
            "best_time": "Wait 1-2 weeks for potential further drops",
            "reasoning": "Price has been trending downwards recently",
        }
    elif trend == "increasing":
        predicted_price = current_price * 0.95
        return {
            "will_drop": True,
            "predicted_price": round(predicted_price, 2),
            "confidence": 0.6,
            "best_time": "Buy now before prices increase further",
            "reasoning": "Price is increasing, but may have seasonal drops",
        }
    else:
        if current_price > lowest_price * 1.1:
            return {
                "will_drop": True,
                "predicted_price": round(lowest_price * 1.05, 2),
                "confidence": 0.5,
                "best_time": "Wait for next sale season",
                "reasoning": "Price is stable but higher than historical low",
            }
        return {
            "will_drop": False,
            "predicted_price": current_price,
            "confidence": 0.7,
            "best_time": "Current price is fair, buy when needed",
            "reasoning": "Price is stable and near historical average",
        }
