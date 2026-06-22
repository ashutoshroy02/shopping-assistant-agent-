import pytest
from agents.price_agent import (
    calculate_price_trend,
    calculate_volatility,
    generate_prediction,
)


class TestCalculatePriceTrend:
    def test_decreasing_trend(self):
        prices = [100, 95, 90, 85, 80]
        trend = calculate_price_trend(prices)
        assert trend == "decreasing"

    def test_increasing_trend(self):
        prices = [80, 85, 90, 95, 100]
        trend = calculate_price_trend(prices)
        assert trend == "increasing"

    def test_stable_trend(self):
        prices = [100, 101, 99, 100, 101]
        trend = calculate_price_trend(prices)
        assert trend == "stable"

    def test_single_price(self):
        prices = [100]
        trend = calculate_price_trend(prices)
        assert trend == "stable"


class TestCalculateVolatility:
    def test_high_volatility(self):
        prices = [100, 150, 80, 130, 90]
        volatility = calculate_volatility(prices)
        assert volatility > 20

    def test_low_volatility(self):
        prices = [100, 101, 99, 100, 101]
        volatility = calculate_volatility(prices)
        assert volatility < 5

    def test_single_price(self):
        prices = [100]
        volatility = calculate_volatility(prices)
        assert volatility == 0.0


class TestGeneratePrediction:
    def test_decreasing_prediction(self):
        prediction = generate_prediction("decreasing", 100, 90)
        assert prediction["will_drop"] is True
        assert prediction["predicted_price"] < 100

    def test_increasing_prediction(self):
        prediction = generate_prediction("increasing", 100, 90)
        assert prediction["predicted_price"] < 100

    def test_stable_higher_than_lowest(self):
        prediction = generate_prediction("stable", 100, 80)
        assert prediction["will_drop"] is True

    def test_stable_near_lowest(self):
        prediction = generate_prediction("stable", 100, 95)
        assert prediction["will_drop"] is False
