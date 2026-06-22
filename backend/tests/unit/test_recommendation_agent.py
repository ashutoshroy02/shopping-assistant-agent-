import pytest
from agents.recommendation_agent import (
    calculate_recommendation_score,
    calculate_use_case_score,
    calculate_value_score,
    categorize_recommendations,
    generate_reasoning,
)


@pytest.fixture
def sample_product():
    return {
        "id": "1",
        "title": "Gaming Laptop",
        "price": 89990,
        "original_price": 99990,
        "rating": 4.5,
        "brand": "ASUS",
        "category": "laptops",
        "review_count": 1250,
    }


@pytest.fixture
def sample_reviews():
    return [
        {
            "product_id": "1",
            "sentiment_score": 0.8,
            "pros": ["Great performance", "Good display"],
            "cons": ["Heavy"],
        }
    ]


@pytest.fixture
def sample_intent():
    return {
        "category": "laptops",
        "budget": {"min": 50000, "max": 100000},
        "brands": ["ASUS", "MSI"],
        "use_case": "gaming",
    }


class TestCalculateRecommendationScore:
    def test_high_rating_bonus(self, sample_product, sample_reviews, sample_intent):
        score = calculate_recommendation_score(sample_product, sample_reviews, sample_intent)
        assert score > 0

    def test_budget_within_range(self, sample_product, sample_reviews, sample_intent):
        score = calculate_recommendation_score(sample_product, sample_reviews, sample_intent)
        assert score > 30

    def test_brand_match_bonus(self, sample_product, sample_reviews, sample_intent):
        score = calculate_recommendation_score(sample_product, sample_reviews, sample_intent)
        assert score >= 40


class TestCalculateValueScore:
    def test_value_calculation(self, sample_product):
        score = calculate_value_score(sample_product)
        assert score > 0
        assert score <= 10

    def test_missing_data(self):
        score = calculate_value_score({"price": 0, "rating": 0})
        assert score == 0.0


class TestCalculateUseCaseScore:
    def test_gaming_use_case(self, sample_product):
        score = calculate_use_case_score(sample_product, "gaming")
        assert score >= 0

    def test_programming_use_case(self, sample_product):
        score = calculate_use_case_score(sample_product, "programming")
        assert score >= 0


class TestCategorizeRecommendations:
    def test_categories_exist(self):
        recommendations = [
            {"product_id": "1", "price": 50000, "score": 0.9},
            {"product_id": "2", "price": 80000, "score": 0.8},
            {"product_id": "3", "price": 100000, "score": 0.7},
        ]
        categories = categorize_recommendations(recommendations)
        assert "best_overall" in categories
        assert "budget_pick" in categories
        assert "premium_choice" in categories

    def test_empty_recommendations(self):
        categories = categorize_recommendations([])
        assert categories == {}


class TestGenerateReasoning:
    def test_high_rating_reasoning(self, sample_product, sample_reviews, sample_intent):
        reasoning = generate_reasoning(sample_product, sample_reviews, sample_intent, 80)
        assert "recommended" in reasoning.lower()
        assert "rating" in reasoning.lower()

    def test_budget_reasoning(self, sample_product, sample_reviews, sample_intent):
        reasoning = generate_reasoning(sample_product, sample_reviews, sample_intent, 70)
        assert "recommended" in reasoning.lower()
