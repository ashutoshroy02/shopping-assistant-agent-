from typing import Any


async def reflect_on_output(state: dict[str, Any]) -> dict[str, Any]:
    recommendations = state.get("recommendations", [])
    products = state.get("products", [])
    intent = state.get("intent", {})
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)

    validation_result = validate_recommendations(
        recommendations, products, intent, retry_count, max_retries
    )

    if validation_result["should_retry"] and retry_count < max_retries:
        return {
            "reflection_result": {
                "valid": False,
                "should_retry": True,
                "issues": validation_result["issues"],
            },
            "retry_count": retry_count + 1,
        }

    final_response = generate_final_response(state, validation_result)

    return {
        "reflection_result": {
            "valid": True,
            "should_retry": False,
            "issues": validation_result["issues"],
            "quality_score": validation_result["quality_score"],
        },
        "final_response": final_response,
    }


def validate_recommendations(
    recommendations: list[dict],
    products: list[dict],
    intent: dict,
    retry_count: int,
    max_retries: int,
) -> dict[str, Any]:
    issues = []
    quality_score = 100

    if not recommendations:
        issues.append("No recommendations generated")
        quality_score -= 50

    if not products:
        issues.append("No products found")
        quality_score -= 30

    budget = intent.get("budget") or {}
    if budget.get("max") and recommendations:
        max_budget = budget["max"]
        within_budget = sum(
            1 for r in recommendations if r.get("price", 0) <= max_budget
        )
        if within_budget == 0:
            issues.append("No recommendations within budget")
            quality_score -= 40
        elif within_budget < len(recommendations) * 0.5:
            issues.append("Less than half of recommendations within budget")
            quality_score -= 15

    for rec in recommendations:
        if not rec.get("title"):
            issues.append(f"Missing title for product {rec.get('product_id')}")
            quality_score -= 5
        if not rec.get("price"):
            issues.append(f"Missing price for product {rec.get('product_id')}")
            quality_score -= 5
        if rec.get("score", 0) < 0.3:
            issues.append(f"Low quality score for {rec.get('title')}")
            quality_score -= 10

    if intent.get("brands"):
        brand_products = sum(
            1
            for r in recommendations
            if r.get("brand", "").lower() in [b.lower() for b in intent["brands"]]
        )
        if brand_products == 0 and recommendations:
            issues.append("No recommendations match preferred brands")
            quality_score -= 10

    should_retry = quality_score < 60 and retry_count < max_retries

    return {
        "valid": quality_score >= 60,
        "issues": issues,
        "quality_score": max(0, quality_score),
        "should_retry": should_retry,
    }


def generate_final_response(state: dict[str, Any], validation: dict) -> str:
    recommendations = state.get("recommendations", [])
    intent = state.get("intent", {})
    deals = state.get("deals", [])
    price_insights = state.get("price_insights", {})

    response_parts = []

    if intent.get("category"):
        response_parts.append(
            f"I found several great options for {intent['category']}"
        )
    else:
        response_parts.append("I found some great options for you")

    budget = intent.get("budget") or {}
    if budget.get("max"):
        response_parts.append(
            f"within your budget of Rs.{budget['max']:,.0f}"
        )

    response_parts.append("")

    if recommendations:
        response_parts.append("**Top Recommendations:**")
        for i, rec in enumerate(recommendations[:3], 1):
            price_str = f"Rs.{rec.get('price', 0):,.0f}"
            rating_str = f"{rec.get('rating', 'N/A')}/5"
            response_parts.append(
                f"{i}. **{rec.get('title', 'Unknown')}** - {price_str} ({rating_str})"
            )
            if rec.get("reasoning"):
                response_parts.append(f"   {rec['reasoning']}")
        response_parts.append("")

    if deals:
        response_parts.append("**Best Deals:**")
        for deal in deals[:2]:
            response_parts.append(f"- {deal.get('description', '')}")
        response_parts.append("")

    if price_insights:
        first_product_id = list(price_insights.keys())[0] if price_insights else None
        if first_product_id:
            insight = price_insights[first_product_id]
            trend = insight.get("price_trend", "stable")
            if trend == "decreasing":
                response_parts.append(
                    "**Price Insight:** Prices are trending down - consider waiting for a better deal."
                )
            elif trend == "increasing":
                response_parts.append(
                    "**Price Insight:** Prices are going up - buy now to avoid higher prices."
                )

    if validation.get("issues"):
        response_parts.append("")
        response_parts.append(
            "*Note: Some limitations in available data may affect recommendations.*"
        )

    return "\n".join(response_parts)
