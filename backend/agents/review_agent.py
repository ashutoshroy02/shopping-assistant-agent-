from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import async_session_factory
from database.models import Review


async def analyze_reviews(state: dict[str, Any]) -> dict[str, Any]:
    products = state.get("products", [])

    async with async_session_factory() as db:
        reviews_data = []

        for product in products[:5]:
            product_id = product.get("id")

            query = (
                select(Review)
                .where(Review.product_id == product_id)
                .order_by(Review.created_at.desc())
                .limit(50)
            )

            result = await db.execute(query)
            reviews = result.scalars().all()

            if reviews:
                sentiments = [r.sentiment_score for r in reviews if r.sentiment_score]
                ratings = [r.rating for r in reviews if r.rating]

                avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
                avg_rating = sum(ratings) / len(ratings) if ratings else 0

                positive_count = sum(1 for s in sentiments if s > 0.3)
                negative_count = sum(1 for s in sentiments if s < -0.3)

                pros, cons = extract_pros_cons(reviews)

                reviews_data.append({
                    "product_id": product_id,
                    "product_title": product.get("title"),
                    "total_reviews": len(reviews),
                    "average_rating": round(avg_rating, 2),
                    "sentiment_score": round(avg_sentiment, 3),
                    "positive_percentage": round(
                        (positive_count / len(sentiments) * 100) if sentiments else 0, 1
                    ),
                    "negative_percentage": round(
                        (negative_count / len(sentiments) * 100) if sentiments else 0, 1
                    ),
                    "pros": pros[:5],
                    "cons": cons[:5],
                    "summary": generate_review_summary(reviews, avg_sentiment),
                })
            else:
                reviews_data.append({
                    "product_id": product_id,
                    "product_title": product.get("title"),
                    "total_reviews": 0,
                    "average_rating": 0,
                    "sentiment_score": 0,
                    "positive_percentage": 0,
                    "negative_percentage": 0,
                    "pros": [],
                    "cons": [],
                    "summary": "No reviews available",
                })

    return {"reviews": reviews_data}


def extract_pros_cons(reviews: list) -> tuple[list[str], list[str]]:
    pros = []
    cons = []

    positive_keywords = [
        "excellent", "great", "amazing", "love", "best", "perfect",
        "recommend", "worth", "fast", "smooth", "comfortable",
    ]
    negative_keywords = [
        "bad", "poor", "terrible", "hate", "worst", "slow",
        "expensive", "broken", "defect", "issue", "problem",
    ]

    for review in reviews:
        text = (review.review_text or "").lower()
        if review.sentiment_score and review.sentiment_score > 0.3:
            for keyword in positive_keywords:
                if keyword in text and keyword.title() not in pros:
                    pros.append(keyword.title())
        elif review.sentiment_score and review.sentiment_score < -0.3:
            for keyword in negative_keywords:
                if keyword in text and keyword.title() not in cons:
                    cons.append(keyword.title())

    return pros[:5], cons[:5]


def generate_review_summary(reviews: list, avg_sentiment: float) -> str:
    if not reviews:
        return "No reviews available"

    total = len(reviews)
    if avg_sentiment > 0.5:
        return f"Highly positive reviews ({total} reviews). Users are very satisfied."
    elif avg_sentiment > 0.2:
        return f"Mostly positive reviews ({total} reviews). Users generally like this product."
    elif avg_sentiment > -0.2:
        return f"Mixed reviews ({total} reviews). Some users satisfied, others have concerns."
    elif avg_sentiment > -0.5:
        return f"Mostly negative reviews ({total} reviews). Users have several complaints."
    else:
        return f"Very negative reviews ({total} reviews). Not recommended by most users."
