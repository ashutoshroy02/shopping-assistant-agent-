from typing import Any


async def compare_products(state: dict[str, Any]) -> dict[str, Any]:
    products = state.get("products", [])
    reviews = state.get("reviews", [])

    if len(products) < 2:
        return {
            "comparison": {
                "products": [],
                "feature_comparison": {},
                "winner": None,
                "reasoning": "Need at least 2 products for comparison",
            }
        }

    comparison_products = []
    for product in products[:5]:
        product_reviews = next(
            (r for r in reviews if r.get("product_id") == product.get("id")),
            None,
        )

        comparison_products.append({
            "id": product.get("id"),
            "title": product.get("title"),
            "price": product.get("price"),
            "original_price": product.get("original_price"),
            "rating": product.get("rating"),
            "review_count": product.get("review_count"),
            "specifications": product.get("specifications", {}),
            "sentiment_score": product_reviews.get("sentiment_score", 0) if product_reviews else 0,
            "pros": product_reviews.get("pros", []) if product_reviews else [],
            "cons": product_reviews.get("cons", []) if product_reviews else [],
        })

    feature_comparison = generate_feature_comparison(comparison_products)
    winner = determine_winner(comparison_products)

    return {
        "comparison": {
            "products": comparison_products,
            "feature_comparison": feature_comparison,
            "winner": winner.get("id") if winner else None,
            "winner_title": winner.get("title") if winner else None,
            "reasoning": generate_comparison_reasoning(comparison_products, winner),
        }
    }


def generate_feature_comparison(products: list[dict]) -> dict[str, dict]:
    comparison = {}

    all_specs = set()
    for product in products:
        all_specs.update(product.get("specifications", {}).keys())

    for spec in all_specs:
        comparison[spec] = {}
        for product in products:
            value = product.get("specifications", {}).get(spec, "N/A")
            comparison[spec][product.get("id")] = value

    comparison["price"] = {p.get("id"): p.get("price") for p in products}
    comparison["rating"] = {p.get("id"): p.get("rating") for p in products}
    comparison["sentiment"] = {p.get("id"): p.get("sentiment_score") for p in products}

    return comparison


def determine_winner(products: list[dict]) -> dict | None:
    if not products:
        return None

    scored_products = []
    for product in products:
        score = 0

        if product.get("rating"):
            score += product["rating"] * 20

        if product.get("sentiment_score"):
            score += product["sentiment_score"] * 10

        if product.get("price") and product.get("rating"):
            value_score = (product["rating"] / product["price"]) * 100000
            score += min(value_score, 30)

        if product.get("review_count"):
            popularity_bonus = min(product["review_count"] / 1000, 10)
            score += popularity_bonus

        scored_products.append((product, score))

    scored_products.sort(key=lambda x: x[1], reverse=True)
    return scored_products[0][0] if scored_products else None


def generate_comparison_reasoning(products: list[dict], winner: dict | None) -> str:
    if not winner:
        return "Unable to determine a clear winner"

    reasons = []

    if winner.get("rating"):
        reasons.append(f"highest rated at {winner['rating']}/5")

    if winner.get("sentiment_score") and winner["sentiment_score"] > 0:
        reasons.append("positive user sentiment")

    if winner.get("pros"):
        reasons.append(f"praised for: {', '.join(winner['pros'][:3])}")

    if winner.get("price"):
        cheapest = min(products, key=lambda p: p.get("price", float("inf")))
        if winner.get("id") == cheapest.get("id"):
            reasons.append("best value for money")
        else:
            reasons.append("best overall package")

    return f"{winner.get('title', 'This product')} is recommended because it has {' and '.join(reasons)}."
