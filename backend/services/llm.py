from typing import Any

from openai import AsyncOpenAI

from config import get_settings

settings = get_settings()

llm_client = AsyncOpenAI(
    api_key=settings.GROQ_API_KEY or "dummy",
    base_url=settings.GROQ_BASE_URL,
)


async def generate_response(
    prompt: str,
    system_prompt: str = "",
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> str:
    if not settings.GROQ_API_KEY:
        return ""

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        response = await llm_client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
    except Exception:
        return ""


async def analyze_sentiment(text: str) -> dict[str, Any]:
    if not settings.GROQ_API_KEY:
        positive_words = ["excellent", "great", "amazing", "love", "best", "perfect", "good"]
        negative_words = ["bad", "poor", "terrible", "hate", "worst", "slow", "broken"]

        text_lower = text.lower()
        pos = sum(1 for w in positive_words if w in text_lower)
        neg = sum(1 for w in negative_words if w in text_lower)
        total = pos + neg
        score = (pos - neg) / total if total > 0 else 0

        return {
            "sentiment_score": round(score, 3),
            "label": "positive" if score > 0.2 else ("negative" if score < -0.2 else "neutral"),
            "pros": [w for w in positive_words if w in text_lower],
            "cons": [w for w in negative_words if w in text_lower],
        }

    prompt = f"""Analyze the sentiment of this product review and return JSON:
{{
    "sentiment_score": float (-1 to 1),
    "label": "positive" | "negative" | "neutral",
    "pros": ["list of pros mentioned"],
    "cons": ["list of cons mentioned"]
}}

Review: {text}"""

    response = await generate_response(prompt, temperature=0.3)
    try:
        import json, re
        json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {"sentiment_score": 0, "label": "neutral", "pros": [], "cons": []}
    except Exception:
        return {"sentiment_score": 0, "label": "neutral", "pros": [], "cons": []}


async def generate_recommendation_reasoning(
    product: dict,
    user_query: str,
    budget: float | None = None,
) -> str:
    if not settings.GROQ_API_KEY:
        reasons = []
        if product.get("rating") and product["rating"] >= 4.0:
            reasons.append(f"rated {product['rating']}/5")
        if budget and product.get("price", 0) <= budget:
            reasons.append("within your budget")
        return f"Recommended because: {', '.join(reasons)}." if reasons else "Good overall value."

    prompt = f"""User query: {user_query}
Product: {product.get('title', 'Unknown')}
Price: ₹{product.get('price', 0)}
Rating: {product.get('rating', 'N/A')}/5

Write a 1-2 sentence recommendation reason."""

    return await generate_response(prompt, temperature=0.5, max_tokens=200)
