import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.middleware.error_handler import NotFoundException, ValidationException
from api.routes.auth import get_current_user
from database.connection import get_db
from database.models import Product, SavedProduct, User

router = APIRouter()


@router.get("")
async def list_saved_products(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SavedProduct, Product)
        .join(Product, SavedProduct.product_id == Product.id)
        .where(SavedProduct.user_id == user.id)
        .order_by(SavedProduct.saved_at.desc())
    )
    rows = result.all()

    return {
        "products": [
            {
                "id": str(product.id),
                "title": product.title,
                "price": product.price,
                "rating": product.rating,
                "brand": product.brand,
                "category": product.category,
                "saved_at": saved.saved_at.isoformat(),
            }
            for saved, product in rows
        ],
        "total": len(rows),
    }


@router.post("/{product_id}", status_code=201)
async def save_product(
    product_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise NotFoundException("Product not found")

    existing = await db.execute(
        select(SavedProduct).where(
            SavedProduct.user_id == user.id,
            SavedProduct.product_id == product_id,
        )
    )
    if existing.scalar_one_or_none():
        raise ValidationException("Product already saved")

    saved = SavedProduct(user_id=user.id, product_id=product_id)
    db.add(saved)
    await db.flush()

    return {"message": "Product saved successfully", "product_id": str(product_id)}


@router.delete("/{product_id}")
async def unsave_product(
    product_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SavedProduct).where(
            SavedProduct.user_id == user.id,
            SavedProduct.product_id == product_id,
        )
    )
    saved = result.scalar_one_or_none()
    if not saved:
        raise NotFoundException("Saved product not found")

    await db.delete(saved)
    await db.flush()

    return {"message": "Product removed from saved list"}


@router.get("/check/{product_id}")
async def check_saved(
    product_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SavedProduct).where(
            SavedProduct.user_id == user.id,
            SavedProduct.product_id == product_id,
        )
    )
    saved = result.scalar_one_or_none()

    return {"is_saved": saved is not None}
