import pytest
from agents.reflection_agent import (
    generate_final_response,
    validate_recommendations,
)


@pytest.fixture
def valid_state():
    return {
        "recommendations": [
            {
                "product_id": "1",
                "title": "Gaming Laptop",
                "price": 89990,
                "rating": 4.5,
                "score": 0.9,
                "reasoning": "Great value",
            }
        ],
        "products": [
            {"id": "1", "title": "Gaming Laptop", "price": 89990}
        ],
        "intent": {"budget": {"max": 100000}, "category": "laptops"},
        "deals": [{"description": "10% off"}],
        "price_insights": {
            "1": {"price_trend": "stable", "current_price": 89990}
        },
    }


@pytest.fixture
def invalid_state():
    return {
        "recommendations": [],
        "products": [],
        "intent": {"budget": {"max": 50000}},
        "deals": [],
        "price_insights": {},
    }


class TestValidateRecommendations:
    def test_valid_recommendations(self, valid_state):
        result = validate_recommendations(
            valid_state["recommendations"],
            valid_state["products"],
            valid_state["intent"],
            0,
            3,
        )
        assert result["valid"] is True
        assert result["quality_score"] >= 60

    def test_empty_recommendations(self, invalid_state):
        result = validate_recommendations(
            invalid_state["recommendations"],
            invalid_state["products"],
            invalid_state["intent"],
            0,
            3,
        )
        assert result["valid"] is False
        assert result["should_retry"] is True

    def test_budget_violation(self):
        recommendations = [
            {"product_id": "1", "title": "Expensive", "price": 200000, "score": 0.5}
        ]
        intent = {"budget": {"max": 100000}}
        result = validate_recommendations(recommendations, [], intent, 0, 3)
        assert result["quality_score"] < 80

    def test_retry_limit(self, valid_state):
        result = validate_recommendations(
            valid_state["recommendations"],
            valid_state["products"],
            valid_state["intent"],
            3,
            3,
        )
        assert result["should_retry"] is False


class TestGenerateFinalResponse:
    def test_response_with_recommendations(self, valid_state):
        validation = {"valid": True, "issues": []}
        response = generate_final_response(valid_state, validation)
        assert "Gaming Laptop" in response
        assert "₹89,990" in response

    def test_response_with_deals(self, valid_state):
        validation = {"valid": True, "issues": []}
        response = generate_final_response(valid_state, validation)
        assert "Deal" in response or "discount" in response.lower()

    def test_empty_state(self):
        state = {
            "recommendations": [],
            "products": [],
            "intent": {},
            "deals": [],
            "price_insights": {},
        }
        validation = {"valid": True, "issues": []}
        response = generate_final_response(state, validation)
        assert isinstance(response, str)
