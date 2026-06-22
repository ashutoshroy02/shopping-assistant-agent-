import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import async_session_factory
from database.models import Review
from mcp_servers.base import MCPServer

review_server = MCPServer("review")


@review_server.tool(
    name="fetch_reviews",
    description="Fetch reviews for a specific product",
)
async def fetch_reviews(
    product_id: str,
    limit: int = 50,
    sort_by: str = "newest",
) -> dict[str, Any]:
    async with async_session_factory() as db:
        stmt = select(Review).where(Review.product_id == uuid.UUID(product_id))

        if sort_by == "newest":
            stmt = stmt.order_by(Review.created_at.desc())
        elif sort_by == "highest":
            stmt = stmt.order_by(Review.rating.desc())
        elif sort_by == "lowest":
            stmt = stmt.order_by(Review.rating.asc())

        stmt = stmt.limit(limit)

        result = await db.execute(stmt)
        reviews = result.scalars().all()

        return {
            "reviews": [
                {
                    "id": str(r.id),
                    "review_text": r.review_text,
                    "rating": r.rating,
                    "sentiment_score": r.sentiment_score,
                    "source": r.source,
                    "created_at": r.created_at.isoformat(),
                }
                for r in reviews
            ],
            "total": len(reviews),
        }


@review_server.tool(
    name="summarize_reviews",
    description="Get a summary of reviews for a product",
)
async def summarize_reviews(product_id: str) -> dict[str, Any]:
    async with async_session_factory() as db:
        stmt = select(Review).where(Review.product_id == uuid.UUID(product_id))
        result = await db.execute(stmt)
        reviews = result.scalars().all()

        if not reviews:
            return {
                "summary": "No reviews available",
                "total_reviews": 0,
                "average_rating": 0,
                "sentiment_distribution": {},
            }

        ratings = [r.rating for r in reviews if r.rating]
        sentiments = [r.sentiment_score for r in reviews if r.sentiment_score]

        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

        positive = sum(1 for s in sentiments if s > 0.3)
        negative = sum(1 for s in sentiments if s < -0.3)
        neutral = len(sentiments) - positive - negative

        return {
            "summary": generate_summary(reviews, avg_sentiment),
            "total_reviews": len(reviews),
            "average_rating": round(avg_rating, 2),
            "average_sentiment": round(avg_sentiment, 3),
            "sentiment_distribution": {
                "positive": positive,
                "neutral": neutral,
                "negative": negative,
            },
        }


@review_server.tool(
    name="analyze_sentiment",
    description="Analyze sentiment of a review text",
)
async def analyze_sentiment(review_text: str) -> dict[str, Any]:
    positive_words = [
        "excellent", "great", "amazing", "love", "best", "perfect",
        "recommend", "worth", "fast", "smooth", "comfortable", "good",
    ]
    negative_words = [
        "bad", "poor", "terrible", "hate", "worst", "slow",
        "expensive", "broken", "defect", "issue", "problem", "disappointing",
    ]

    text_lower = review_text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    total = positive_count + negative_count
    if total == 0:
        sentiment = 0.0
    else:
        sentiment = (positive_count - negative_count) / total

    return {
        "sentiment_score": round(sentiment, 3),
        "label": "positive" if sentiment > 0.2 else ("negative" if sentiment < -0.2 else "neutral"),
        "confidence": round(min(total / 10, 1.0), 2),
    }


def generate_summary(reviews: list, avg_sentiment: float) -> str:
    if not reviews:
        return "No reviews available"

    total = len(reviews)
    if avg_sentiment > 0.5:
        return f"Highly positive reviews ({total} reviews). Users are very satisfied with this product."
    elif avg_sentiment > 0.2:
        return f"Mostly positive reviews ({total} reviews). Users generally like this product."
    elif avg_sentiment > -0.2:
        return f"Mixed reviews ({total} reviews). Some users satisfied, others have concerns."
    elif avg_sentiment > -0.5:
        return f"Mostly negative reviews ({total} reviews). Users have several complaints."
    else:
        return f"Very negative reviews ({total} reviews). Not recommended by most users."
