import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.middleware.error_handler import NotFoundException
from api.routes.auth import get_current_user
from database.connection import get_db
from database.models import PriceHistory, PriceTracking, Product, SavedProduct, User
from database.schemas import (
    CompareRequest,
    CompareResponse,
    PriceTrackingCreate,
    PriceTrackingResponse,
    ProductResponse,
    RecommendRequest,
    RecommendResponse,
)

router = APIRouter()


@router.get("", response_model=list[ProductResponse])
async def list_products(
    db: AsyncSession = Depends(get_db),
    category: str | None = None,
    brand: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    sort_by: str = Query(default="rating", pattern="^(rating|price|newest)$"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    query = select(Product).where(Product.availability == True)

    if category:
        query = query.where(Product.category == category)
    if brand:
        query = query.where(Product.brand.ilike(f"%{brand}%"))
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    if search:
        query = query.where(
            Product.title.ilike(f"%{search}%")
            | Product.description.ilike(f"%{search}%")
        )

    if sort_by == "rating":
        query = query.order_by(Product.rating.desc().nullslast())
    elif sort_by == "price":
        query = query.order_by(Product.price.asc())
    elif sort_by == "newest":
        query = query.order_by(Product.created_at.desc())

    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    products = result.scalars().all()

    return products


@router.get("/categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product.category, func.count(Product.id))
        .where(Product.availability == True)
        .group_by(Product.category)
    )
    categories = [{"name": row[0], "count": row[1]} for row in result.all()]
    return {"categories": categories}


@router.get("/brands")
async def list_brands(
    db: AsyncSession = Depends(get_db),
    category: str | None = None,
):
    query = select(Product.brand, func.count(Product.id)).where(
        Product.availability == True
    )
    if category:
        query = query.where(Product.category == category)
    query = query.group_by(Product.brand)

    result = await db.execute(query)
    brands = [{"name": row[0], "count": row[1]} for row in result.all()]
    return {"brands": brands}


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise NotFoundException("Product not found")
    return product


@router.get("/{product_id}/similar")
async def get_similar_products(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=5, ge=1, le=20),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise NotFoundException("Product not found")

    query = (
        select(Product)
        .where(Product.category == product.category)
        .where(Product.id != product_id)
        .where(Product.availability == True)
        .order_by(Product.rating.desc().nullslast())
        .limit(limit)
    )

    result = await db.execute(query)
    similar_products = result.scalars().all()

    return {
        "products": [
            {
                "id": str(p.id),
                "title": p.title,
                "price": p.price,
                "rating": p.rating,
                "brand": p.brand,
            }
            for p in similar_products
        ]
    }


@router.post("/recommend", response_model=RecommendResponse)
async def recommend_products(
    request: RecommendRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Product).where(Product.availability == True)

    if request.category:
        query = query.where(Product.category == request.category)

    if request.budget:
        if "max" in request.budget:
            query = query.where(Product.price <= request.budget["max"])
        if "min" in request.budget:
            query = query.where(Product.price >= request.budget["min"])

    if request.preferences and request.preferences.get("brands"):
        brands = request.preferences["brands"]
        query = query.where(Product.brand.ilikeAny([f"%{b}%" for b in brands]))

    query = query.order_by(Product.rating.desc().nullslast()).limit(request.limit)

    result = await db.execute(query)
    products = result.scalars().all()

    recommendations = []
    for i, product in enumerate(products):
        score = max(0.5, 1.0 - (i * 0.1))
        recommendations.append(
            {
                "product_id": str(product.id),
                "title": product.title,
                "price": product.price,
                "rating": product.rating,
                "score": score,
                "reasoning": f"Recommended based on your preferences in {request.category}",
            }
        )

    best_overall = recommendations[0]["product_id"] if recommendations else None
    budget_pick = (
        min(recommendations, key=lambda x: x["price"])["product_id"]
        if recommendations
        else None
    )
    premium_choice = (
        max(recommendations, key=lambda x: x["price"])["product_id"]
        if recommendations
        else None
    )

    return RecommendResponse(
        recommendations=recommendations,
        categories={
            "best_overall": best_overall,
            "budget_pick": budget_pick,
            "premium_choice": premium_choice,
        },
    )


@router.post("/compare", response_model=CompareResponse)
async def compare_products(
    request: CompareRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Product).where(Product.id.in_(request.product_ids))
    )
    products = result.scalars().all()

    if len(products) < 2:
        raise NotFoundException("At least 2 products required for comparison")

    comparison_products = []
    for product in products:
        comparison_products.append(
            {
                "id": str(product.id),
                "title": product.title,
                "price": product.price,
                "original_price": product.original_price,
                "rating": product.rating,
                "review_count": product.review_count,
                "brand": product.brand,
                "specifications": product.specifications,
            }
        )

    all_specs = set()
    for p in comparison_products:
        all_specs.update(p.get("specifications", {}).keys())

    feature_comparison = {}
    for spec in all_specs:
        feature_comparison[spec] = {}
        for p in comparison_products:
            feature_comparison[spec][p["id"]] = p.get("specifications", {}).get(spec, "N/A")

    best_product = max(products, key=lambda p: p.rating or 0)

    return CompareResponse(
        comparison={
            "products": comparison_products,
            "feature_comparison": feature_comparison,
            "analysis": {
                "winner": str(best_product.id),
                "reasoning": f"Best rated product with {best_product.rating}/5 stars",
            },
        }
    )


@router.post("/track-price", response_model=PriceTrackingResponse, status_code=201)
async def track_price(
    request: PriceTrackingCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Product).where(Product.id == request.product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise NotFoundException("Product not found")

    existing = await db.execute(
        select(PriceTracking).where(
            PriceTracking.user_id == user.id,
            PriceTracking.product_id == request.product_id,
        )
    )
    if existing.scalar_one_or_none():
        from api.middleware.error_handler import ValidationException
        raise ValidationException("Already tracking this product")

    tracking = PriceTracking(
        user_id=user.id,
        product_id=request.product_id,
        target_price=request.target_price,
        alert_on_drop=request.alert_on_drop,
    )
    db.add(tracking)
    await db.flush()
    await db.refresh(tracking)

    return PriceTrackingResponse(
        id=tracking.id,
        user_id=tracking.user_id,
        product_id=tracking.product_id,
        target_price=tracking.target_price,
        current_price=product.price,
        status=tracking.status,
        created_at=tracking.created_at,
    )


@router.delete("/track-price/{product_id}")
async def stop_tracking(
    product_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(PriceTracking).where(
            PriceTracking.user_id == user.id,
            PriceTracking.product_id == product_id,
        )
    )
    tracking = result.scalar_one_or_none()
    if not tracking:
        raise NotFoundException("Price tracking not found")

    await db.delete(tracking)
    await db.flush()

    return {"message": "Price tracking stopped"}


@router.get("/tracked", response_model=list[PriceTrackingResponse])
async def list_tracked_products(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(PriceTracking, Product)
        .join(Product, PriceTracking.product_id == Product.id)
        .where(PriceTracking.user_id == user.id)
        .order_by(PriceTracking.created_at.desc())
    )
    rows = result.all()

    return [
        PriceTrackingResponse(
            id=tracking.id,
            user_id=tracking.user_id,
            product_id=tracking.product_id,
            target_price=tracking.target_price,
            current_price=product.price,
            status=tracking.status,
            created_at=tracking.created_at,
        )
        for tracking, product in rows
    ]


@router.get("/price-history/{product_id}")
async def get_price_history(
    product_id: uuid.UUID,
    period: str = Query(default="30d", pattern="^(7d|30d|90d|1y)$"),
    source: str = Query(default="all"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise NotFoundException("Product not found")

    period_days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}
    start_date = datetime.utcnow() - timedelta(days=period_days[period])

    query = (
        select(PriceHistory)
        .where(PriceHistory.product_id == product_id)
        .where(PriceHistory.recorded_at >= start_date)
    )

    if source != "all":
        query = query.where(PriceHistory.source == source)

    query = query.order_by(PriceHistory.recorded_at.desc())

    result = await db.execute(query)
    history = result.scalars().all()

    prices = [h.price for h in history]
    statistics = {
        "current": product.price,
        "lowest": min(prices) if prices else product.price,
        "highest": max(prices) if prices else product.price,
        "average": round(sum(prices) / len(prices), 2) if prices else product.price,
        "trend": "stable",
    }

    if len(prices) >= 2:
        recent_avg = sum(prices[:3]) / min(len(prices), 3)
        older_avg = sum(prices[-3:]) / min(len(prices), 3) if len(prices) >= 3 else prices[-1]
        if recent_avg < older_avg * 0.95:
            statistics["trend"] = "decreasing"
        elif recent_avg > older_avg * 1.05:
            statistics["trend"] = "increasing"

    return {
        "product_id": str(product_id),
        "product_title": product.title,
        "current_price": product.price,
        "history": [
            {
                "price": h.price,
                "source": h.source,
                "timestamp": h.recorded_at.isoformat(),
            }
            for h in history
        ],
        "statistics": statistics,
    }
