from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.middleware.error_handler import NotFoundException
from api.routes.auth import get_current_user
from database.connection import get_db
from database.models import (
    ChatSession,
    PriceTracking,
    Product,
    Recommendation,
    SavedProduct,
    SearchHistory,
    User,
)

router = APIRouter()


@router.get("")
async def get_analytics(
    period: str = Query(default="30d", pattern="^(7d|30d|90d)$"),
    type: str = Query(default="all", pattern="^(user|platform|all)$"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    period_days = {"7d": 7, "30d": 30, "90d": 90}
    start_date = datetime.utcnow() - timedelta(days=period_days[period])

    user_analytics = {}
    if type in ("user", "all"):
        searches_result = await db.execute(
            select(func.count(SearchHistory.id)).where(
                SearchHistory.user_id == user.id,
                SearchHistory.searched_at >= start_date,
            )
        )
        total_searches = searches_result.scalar() or 0

        saved_result = await db.execute(
            select(func.count(SavedProduct.id)).where(SavedProduct.user_id == user.id)
        )
        saved_products = saved_result.scalar() or 0

        chats_result = await db.execute(
            select(func.count(ChatSession.id)).where(
                ChatSession.user_id == user.id,
                ChatSession.created_at >= start_date,
            )
        )
        total_chats = chats_result.scalar() or 0

        tracked_result = await db.execute(
            select(func.count(PriceTracking.id)).where(
                PriceTracking.user_id == user.id,
                PriceTracking.status == "active",
            )
        )
        tracked_products = tracked_result.scalar() or 0

        categories_result = await db.execute(
            select(SearchHistory.filters).where(
                SearchHistory.user_id == user.id,
                SearchHistory.searched_at >= start_date,
            )
        )
        categories = list(
            set(
                f.get("category", "unknown")
                for f in categories_result.scalars().all()
                if f
            )
        )

        user_analytics = {
            "total_searches": total_searches,
            "saved_products": saved_products,
            "total_chats": total_chats,
            "tracked_products": tracked_products,
            "categories_viewed": categories[:10],
        }

    platform_analytics = {}
    if type in ("platform", "all"):
        users_result = await db.execute(select(func.count(User.id)))
        total_users = users_result.scalar() or 0

        products_result = await db.execute(select(func.count(Product.id)))
        total_products = products_result.scalar() or 0

        recommendations_result = await db.execute(
            select(func.count(Recommendation.id))
        )
        total_recommendations = recommendations_result.scalar() or 0

        popular_categories_result = await db.execute(
            select(Product.category, func.count(Product.id))
            .where(Product.availability == True)
            .group_by(Product.category)
            .order_by(func.count(Product.id).desc())
            .limit(5)
        )
        popular_categories = [
            {"name": row[0], "count": row[1]}
            for row in popular_categories_result.all()
        ]

        top_rated_result = await db.execute(
            select(Product)
            .where(Product.availability == True, Product.rating.isnot(None))
            .order_by(Product.rating.desc())
            .limit(5)
        )
        top_rated = [
            {
                "id": str(p.id),
                "title": p.title,
                "rating": p.rating,
                "price": p.price,
            }
            for p in top_rated_result.scalars().all()
        ]

        platform_analytics = {
            "total_users": total_users,
            "total_products": total_products,
            "total_recommendations": total_recommendations,
            "popular_categories": popular_categories,
            "top_rated_products": top_rated,
        }

    return {
        "user_analytics": user_analytics,
        "platform_analytics": platform_analytics,
    }


@router.get("/trends")
async def get_search_trends(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=50),
):
    result = await db.execute(
        select(SearchHistory.query, func.count(SearchHistory.id))
        .where(SearchHistory.user_id == user.id)
        .group_by(SearchHistory.query)
        .order_by(func.count(SearchHistory.id).desc())
        .limit(limit)
    )
    trends = [{"query": row[0], "count": row[1]} for row in result.all()]

    return {"trends": trends}
