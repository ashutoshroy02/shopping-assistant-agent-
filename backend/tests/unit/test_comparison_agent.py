import pytest
from agents.comparison_agent import (
    determine_winner,
    generate_comparison_reasoning,
    generate_feature_comparison,
)


@pytest.fixture
def sample_products():
    return [
        {
            "id": "1",
            "title": "Product A",
            "price": 50000,
            "rating": 4.5,
            "specifications": {"ram": "16GB", "storage": "512GB"},
            "sentiment_score": 0.8,
            "pros": ["Good performance", "Great display"],
            "cons": ["Heavy"],
        },
        {
            "id": "2",
            "title": "Product B",
            "price": 60000,
            "rating": 4.3,
            "specifications": {"ram": "32GB", "storage": "1TB"},
            "sentiment_score": 0.6,
            "pros": ["Lightweight", "Good battery"],
            "cons": ["Expensive"],
        },
    ]


class TestGenerateFeatureComparison:
    def test_basic_comparison(self, sample_products):
        result = generate_feature_comparison(sample_products)
        assert "price" in result
        assert "rating" in result
        assert "ram" in result
        assert "storage" in result

    def test_price_values(self, sample_products):
        result = generate_feature_comparison(sample_products)
        assert result["price"]["1"] == 50000
        assert result["price"]["2"] == 60000

    def test_rating_values(self, sample_products):
        result = generate_feature_comparison(sample_products)
        assert result["rating"]["1"] == 4.5
        assert result["rating"]["2"] == 4.3


class TestDetermineWinner:
    def test_winner_exists(self, sample_products):
        winner = determine_winner(sample_products)
        assert winner is not None
        assert "id" in winner

    def test_winner_is_product(self, sample_products):
        winner = determine_winner(sample_products)
        assert winner["id"] in ["1", "2"]

    def test_empty_products(self):
        winner = determine_winner([])
        assert winner is None


class TestGenerateComparisonReasoning:
    def test_with_winner(self, sample_products):
        winner = sample_products[0]
        reasoning = generate_comparison_reasoning(sample_products, winner)
        assert "Product A" in reasoning
        assert "reasoning" in reasoning.lower() or "because" in reasoning.lower()

    def test_without_winner(self, sample_products):
        reasoning = generate_comparison_reasoning(sample_products, None)
        assert "unable" in reasoning.lower() or "no winner" in reasoning.lower()
