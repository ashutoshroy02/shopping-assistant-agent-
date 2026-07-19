from typing import Any

from services.llm import generate_response


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

    final_response = await generate_final_response(state, validation_result)

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

    should_retry = quality_score < 60 and retry_count < max_retries and len(recommendations) > 0

    return {
        "valid": quality_score >= 60,
        "issues": issues,
        "quality_score": max(0, quality_score),
        "should_retry": should_retry,
    }


async def generate_final_response(state: dict[str, Any], validation: dict) -> str:
    recommendations = state.get("recommendations", [])
    intent = state.get("intent", {})
    deals = state.get("deals", [])
    price_insights = state.get("price_insights", {})
    user_query = state.get("user_query", "")

    is_generic = (
        intent.get("category") == "general"
        and not intent.get("budget")
        and intent.get("use_case") == "general"
    )

    # Fast path: generic query with no products — no LLM
    if not recommendations and is_generic:
        return "Hey! I'm your AI shopping assistant. Tell me what you're looking for and I'll find the best options for you. I can help with:\n\n- **Laptops** (gaming, programming, office)\n- **Smartphones** (photography, gaming, budget)\n- **Headphones**, **tablets**, **cameras**, and more\n\nJust mention a product and your budget!"

    # Fast path: generic query with products — template response
    if recommendations and is_generic:
        response_parts = ["Here are some popular products you might like:\n"]
        for i, rec in enumerate(recommendations[:3], 1):
            price_str = f"₹{rec.get('price', 0):,.0f}"
            rating_str = f"{rec.get('rating', 'N/A')}/5"
            response_parts.append(f"{i}. **{rec.get('title', 'Unknown')}** - {price_str} ({rating_str})")
            if rec.get("reasoning"):
                response_parts.append(f"   {rec['reasoning']}")
        if deals:
            response_parts.append(f"\n**Deals:** {deals[0].get('description', '')}")
        return "\n".join(response_parts)

    # Slow path: specific query — use LLM for natural response
    if not recommendations:
        system_prompt = """You are a friendly AI shopping assistant. The user asked about a product but nothing matched.
Respond warmly, suggest they try different criteria, mention available categories.
Keep it under 80 words."""
        prompt = f'User asked: "{user_query}"\n\nNo matching products. Respond helpfully.'
        llm_response = await generate_response(prompt, system_prompt=system_prompt, temperature=0.7, max_tokens=150)
        if llm_response:
            return llm_response
        return "I couldn't find products matching your criteria. Try searching for laptops, smartphones, headphones, tablets, or cameras with a specific budget!"

    # Build context for LLM
    rec_text = ""
    for i, rec in enumerate(recommendations[:5], 1):
        price_str = f"₹{rec.get('price', 0):,.0f}"
        rating_str = f"{rec.get('rating', 'N/A')}/5"
        rec_text += f"{i}. {rec.get('title', 'Unknown')} - {price_str} ({rating_str})\n"
        if rec.get("reasoning"):
            rec_text += f"   {rec['reasoning']}\n"

    deals_text = ""
    for deal in deals[:3]:
        deals_text += f"- {deal.get('description', '')}\n"

    system_prompt = """You are a helpful shopping assistant. Write a concise, friendly response recommending products.
Use markdown formatting. Keep it under 200 words. Include prices in ₹ (INR). Be conversational but professional."""

    prompt = f"""User asked: "{user_query}"

Category: {intent.get('category', 'general')}
Budget: ₹{intent.get('budget', {}).get('max', 'not specified')}
Use case: {intent.get('use_case', 'general')}

Top recommendations:
{rec_text}

Available deals:
{deals_text}

Write a helpful response with the top 3 recommendations. Include why each is good for the user's needs."""

    llm_response = await generate_response(prompt, system_prompt=system_prompt, temperature=0.7, max_tokens=500)

    if llm_response:
        return llm_response

    # Fallback to template
    response_parts = []
    if intent.get("category"):
        response_parts.append(f"I found several great options for {intent['category']}")
    else:
        response_parts.append("I found some great options for you")

    budget = intent.get("budget") or {}
    if budget.get("max"):
        response_parts.append(f"within your budget of ₹{budget['max']:,.0f}")

    response_parts.append("")

    if recommendations:
        response_parts.append("**Top Recommendations:**")
        for i, rec in enumerate(recommendations[:3], 1):
            price_str = f"₹{rec.get('price', 0):,.0f}"
            rating_str = f"{rec.get('rating', 'N/A')}/5"
            response_parts.append(f"{i}. **{rec.get('title', 'Unknown')}** - {price_str} ({rating_str})")
            if rec.get("reasoning"):
                response_parts.append(f"   {rec['reasoning']}")
        response_parts.append("")

    if deals:
        response_parts.append("**Best Deals:**")
        for deal in deals[:2]:
            response_parts.append(f"- {deal.get('description', '')}")

    return "\n".join(response_parts)
