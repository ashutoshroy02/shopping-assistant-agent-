from typing import Any


async def generate_recommendations(state: dict[str, Any]) -> dict[str, Any]:
    products = state.get("products", [])
    reviews = state.get("reviews", [])
    comparison = state.get("comparison", {})
    intent = state.get("intent", {})

    if not products:
        return {
            "recommendations": [],
            "metadata": {"error": "No products to recommend"},
        }

    scored_products = []
    for product in products:
        score = calculate_recommendation_score(product, reviews, intent)
        reasoning = generate_reasoning(product, reviews, intent, score)

        scored_products.append({
            "product_id": product.get("id"),
            "title": product.get("title"),
            "price": product.get("price"),
            "original_price": product.get("original_price"),
            "rating": product.get("rating"),
            "brand": product.get("brand"),
            "category": product.get("category"),
            "specifications": product.get("specifications"),
            "score": round(score, 3),
            "reasoning": reasoning,
            "value_for_money": calculate_value_score(product),
            "pros": get_product_pros(product, reviews),
            "cons": get_product_cons(product, reviews),
        })

    scored_products.sort(key=lambda x: x["score"], reverse=True)

    categories = categorize_recommendations(scored_products)

    return {
        "recommendations": scored_products[:10],
        "metadata": {
            "total_scored": len(scored_products),
            "categories": categories,
            "intent": intent,
        },
    }


def calculate_recommendation_score(
    product: dict, reviews: list[dict], intent: dict
) -> float:
    score = 0.0

    if product.get("rating"):
        score += (product["rating"] / 5.0) * 30

    product_reviews = next(
        (r for r in reviews if r.get("product_id") == product.get("id")), None
    )
    if product_reviews:
        sentiment = product_reviews.get("sentiment_score", 0)
        score += max(0, sentiment) * 20

    budget = intent.get("budget") or {}
    if product.get("price") and budget.get("max"):
        budget_max = budget["max"]
        price_ratio = product["price"] / budget_max
        if price_ratio <= 0.7:
            score += 15
        elif price_ratio <= 0.9:
            score += 10
        elif price_ratio <= 1.0:
            score += 5

    if intent.get("brands"):
        if product.get("brand", "").lower() in [b.lower() for b in intent["brands"]]:
            score += 10

    if intent.get("use_case"):
        use_case_bonus = calculate_use_case_score(product, intent["use_case"])
        score += use_case_bonus

    if product.get("review_count"):
        popularity = min(product["review_count"] / 1000, 10)
        score += popularity

    return min(score, 100)


def calculate_value_score(product: dict) -> float:
    if not product.get("price") or not product.get("rating"):
        return 0.0

    base_value = (product["rating"] / product["price"]) * 100000
    return round(min(base_value, 10.0), 2)


def calculate_use_case_score(product: dict, use_case: str) -> float:
    specs = product.get("specifications", {})
    specs_str = str(specs).lower()

    use_case_keywords = {
        "gaming": ["gaming", "rtx", "gtx", "144hz", "120hz"],
        "programming": ["ram", "ssd", "processor", "core"],
        "video editing": ["ram", "gpu", "processor", "display"],
        "office": ["lightweight", "battery", "portable"],
        "student": ["budget", "lightweight", "battery"],
        "photography": ["camera", "display", "color"],
    }

    keywords = use_case_keywords.get(use_case, [])
    bonus = 0
    for keyword in keywords:
        if keyword in specs_str:
            bonus += 2

    return min(bonus, 10)


def get_product_pros(product: dict, reviews: list[dict]) -> list[str]:
    product_reviews = next(
        (r for r in reviews if r.get("product_id") == product.get("id")), None
    )
    if product_reviews:
        return product_reviews.get("pros", [])

    pros = []
    if product.get("rating") and product["rating"] >= 4.0:
        pros.append("Highly rated")
    if product.get("price") and product.get("original_price"):
        if product["price"] < product["original_price"]:
            pros.append("Good discount available")
    return pros


def get_product_cons(product: dict, reviews: list[dict]) -> list[str]:
    product_reviews = next(
        (r for r in reviews if r.get("product_id") == product.get("id")), None
    )
    if product_reviews:
        return product_reviews.get("cons", [])
    return []


def generate_reasoning(
    product: dict, reviews: list[dict], intent: dict, score: float
) -> str:
    reasons = []

    if product.get("rating") and product["rating"] >= 4.5:
        reasons.append(f"Excellent rating ({product['rating']}/5)")
    elif product.get("rating") and product["rating"] >= 4.0:
        reasons.append(f"Good rating ({product['rating']}/5)")

    product_reviews = next(
        (r for r in reviews if r.get("product_id") == product.get("id")), None
    )
    if product_reviews:
        sentiment = product_reviews.get("sentiment_score", 0)
        if sentiment > 0.5:
            reasons.append("Very positive user feedback")
        elif sentiment > 0.2:
            reasons.append("Positive user feedback")

    if intent.get("budget") and product.get("price"):
        if product["price"] <= intent["budget"].get("max", float("inf")) * 0.8:
            reasons.append("Well within budget")

    if intent.get("use_case"):
        reasons.append(f"Suitable for {intent['use_case']} use")

    if not reasons:
        reasons.append("Balanced features and price")

    return f"Recommended because: {', '.join(reasons)}."


def categorize_recommendations(scored_products: list[dict]) -> dict[str, str]:
    if not scored_products:
        return {}

    best_overall = scored_products[0]["product_id"] if scored_products else None

    budget_pick = None
    if scored_products:
        budget_products = sorted(scored_products, key=lambda x: x.get("price", 0))
        budget_pick = budget_products[0]["product_id"] if budget_products else None

    premium_choice = None
    if scored_products:
        premium_products = sorted(
            scored_products, key=lambda x: x.get("price", 0), reverse=True
        )
        premium_choice = premium_products[0]["product_id"] if premium_products else None

    return {
        "best_overall": best_overall,
        "budget_pick": budget_pick,
        "premium_choice": premium_choice,
    }
