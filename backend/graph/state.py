from typing import Annotated, Any, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_query: str
    intent: dict[str, Any]
    products: list[dict[str, Any]]
    reviews: list[dict[str, Any]]
    comparison: dict[str, Any]
    recommendations: list[dict[str, Any]]
    deals: list[dict[str, Any]]
    price_insights: dict[str, Any]
    reflection_result: dict[str, Any]
    final_response: str
    metadata: dict[str, Any]
    retry_count: int
    max_retries: int
