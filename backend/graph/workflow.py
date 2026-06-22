from typing import Any, Literal

from langgraph.graph import END, StateGraph

from agents.intent_agent import extract_intent
from agents.search_agent import search_products
from agents.review_agent import analyze_reviews
from agents.comparison_agent import compare_products as compare_products_agent
from agents.recommendation_agent import generate_recommendations
from agents.deal_agent import find_deals
from agents.price_agent import analyze_prices, predict_price_drop
from agents.reflection_agent import reflect_on_output
from graph.state import AgentState


def should_retry(state: AgentState) -> Literal["retry", "end"]:
    reflection = state.get("reflection_result", {})
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)

    if reflection.get("should_retry") and retry_count < max_retries:
        return "retry"
    return "end"


def create_workflow() -> StateGraph:
    workflow = StateGraph(AgentState)

    workflow.add_node("intent", extract_intent)
    workflow.add_node("search", search_products)
    workflow.add_node("reviews", analyze_reviews)
    workflow.add_node("comparison", compare_products_agent)
    workflow.add_node("recommendations", generate_recommendations)
    workflow.add_node("deals", find_deals)
    workflow.add_node("price_analysis", analyze_prices)
    workflow.add_node("price_prediction", predict_price_drop)
    workflow.add_node("reflection", reflect_on_output)

    workflow.set_entry_point("intent")

    workflow.add_edge("intent", "search")
    workflow.add_edge("search", "reviews")
    workflow.add_edge("reviews", "comparison")
    workflow.add_edge("comparison", "recommendations")
    workflow.add_edge("recommendations", "deals")
    workflow.add_edge("deals", "price_analysis")
    workflow.add_edge("price_analysis", "price_prediction")
    workflow.add_edge("price_prediction", "reflection")

    workflow.add_conditional_edges(
        "reflection",
        should_retry,
        {
            "retry": "intent",
            "end": END,
        },
    )

    return workflow.compile()


workflow = create_workflow()


async def execute_workflow(user_query: str, user_id: str | None = None) -> dict[str, Any]:
    initial_state: AgentState = {
        "messages": [],
        "user_query": user_query,
        "intent": {},
        "products": [],
        "reviews": [],
        "comparison": {},
        "recommendations": [],
        "deals": [],
        "price_insights": {},
        "reflection_result": {},
        "final_response": "",
        "metadata": {},
        "retry_count": 0,
        "max_retries": 3,
    }

    result = await workflow.ainvoke(initial_state)

    return {
        "response": result.get("final_response", ""),
        "products": result.get("recommendations", []),
        "metadata": {
            "intent": result.get("intent", {}),
            "products_found": len(result.get("products", [])),
            "deals_found": len(result.get("deals", [])),
            "reflection": result.get("reflection_result", {}),
        },
    }
