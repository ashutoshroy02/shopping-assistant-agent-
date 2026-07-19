from typing import Any

from services.product_search import search_products_online


async def search_products(state: dict[str, Any]) -> dict[str, Any]:
    intent = state.get("intent", {})
    user_query = state.get("user_query", "")

    # Always search with original query for best results
    search_query = user_query

    budget = intent.get("budget") or {}
    if budget.get("max"):
        search_query += f" under {budget['max']} INR"

    search_query += " buy online India"

    # Search real products online
    products_list = await search_products_online(search_query)

    # Filter by budget only if products have real prices
    if budget.get("max") and products_list:
        priced = [p for p in products_list if p.get("price", 0) > 0]
        if priced:
            products_list = [
                p for p in products_list
                if p.get("price", 0) == 0 or p.get("price", 0) <= budget["max"] * 1.1
            ]

    return {
        "products": products_list,
        "metadata": {
            "products_found": len(products_list),
            "search_query": search_query,
            "search_criteria": intent,
        },
    }
