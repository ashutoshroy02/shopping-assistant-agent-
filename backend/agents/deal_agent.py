from typing import Any


async def find_deals(state: dict[str, Any]) -> dict[str, Any]:
    products = state.get("products", [])
    recommendations = state.get("recommendations", [])

    deals = []

    for product in products[:10]:
        product_deals = analyze_product_deals(product)
        if product_deals:
            deals.extend(product_deals)

    for rec in recommendations[:5]:
        rec_deals = analyze_recommendation_deals(rec)
        if rec_deals:
            deals.extend(rec_deals)

    deals.sort(key=lambda x: x.get("discount_percentage", 0), reverse=True)

    return {
        "deals": deals[:10],
        "metadata": {
            "total_deals_found": len(deals),
            "best_deal": deals[0] if deals else None,
        },
    }


def analyze_product_deals(product: dict) -> list[dict[str, Any]]:
    deals = []

    if product.get("price") and product.get("original_price"):
        if product["original_price"] > product["price"]:
            discount = product["original_price"] - product["price"]
            discount_pct = (discount / product["original_price"]) * 100

            deals.append({
                "product_id": product.get("id"),
                "product_title": product.get("title"),
                "deal_type": "price_drop",
                "original_price": product["original_price"],
                "current_price": product["price"],
                "savings": discount,
                "discount_percentage": round(discount_pct, 1),
                "description": f"Save ₹{discount:,.0f} ({discount_pct:.0f}% off)",
            })

    return deals


def analyze_recommendation_deals(recommendation: dict) -> list[dict[str, Any]]:
    deals = []

    if recommendation.get("price") and recommendation.get("original_price"):
        if recommendation["original_price"] > recommendation["price"]:
            discount = recommendation["original_price"] - recommendation["price"]
            discount_pct = (discount / recommendation["original_price"]) * 100

            deals.append({
                "product_id": recommendation.get("product_id"),
                "product_title": recommendation.get("title"),
                "deal_type": "recommended_deal",
                "original_price": recommendation["original_price"],
                "current_price": recommendation["price"],
                "savings": discount,
                "discount_percentage": round(discount_pct, 1),
                "description": f"Best price for this recommended product",
            })

    return deals


async def find_coupons(state: dict[str, Any]) -> dict[str, Any]:
    products = state.get("products", [])

    coupons = []

    for product in products[:5]:
        product_coupons = generate_coupon_suggestions(product)
        coupons.extend(product_coupons)

    return {"coupons": coupons}


def generate_coupon_suggestions(product: dict) -> list[dict[str, Any]]:
    coupons = []

    brand = product.get("brand", "").lower()

    brand_coupons = {
        "apple": [
            {"code": "APPLE10", "discount": "10%", "description": "Apple products discount"},
            {"code": "IPHONE5", "discount": "5%", "description": "iPhone exclusive"},
        ],
        "samsung": [
            {"code": "SAMSUNG15", "discount": "15%", "description": "Samsung store discount"},
            {"code": "GALAXY10", "discount": "10%", "description": "Galaxy series offer"},
        ],
        "asus": [
            {"code": "ASUS10", "discount": "10%", "description": "ASUS products discount"},
        ],
        "lenovo": [
            {"code": "LENOVO12", "discount": "12%", "description": "Lenovo store offer"},
        ],
    }

    if brand in brand_coupons:
        for coupon in brand_coupons[brand]:
            coupons.append({
                "product_id": product.get("id"),
                "product_title": product.get("title"),
                **coupon,
            })

    return coupons


async def find_cashback(state: dict[str, Any]) -> dict[str, Any]:
    products = state.get("products", [])

    cashback_offers = []

    for product in products[:5]:
        if product.get("price", 0) > 50000:
            cashback_pct = 5 if product["price"] > 100000 else 3
            cashback_amount = product["price"] * cashback_pct / 100

            cashback_offers.append({
                "product_id": product.get("id"),
                "product_title": product.get("title"),
                "cashback_percentage": cashback_pct,
                "cashback_amount": round(cashback_amount, 2),
                "description": f"{cashback_pct}% cashback on this purchase",
            })

    return {"cashback_offers": cashback_offers}
