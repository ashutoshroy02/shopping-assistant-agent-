import pytest
from agents.deal_agent import (
    analyze_product_deals,
    generate_coupon_suggestions,
)


@pytest.fixture
def product_with_discount():
    return {
        "id": "1",
        "title": "Gaming Laptop",
        "price": 89990,
        "original_price": 99990,
        "brand": "ASUS",
    }


@pytest.fixture
def product_without_discount():
    return {
        "id": "2",
        "title": "Budget Laptop",
        "price": 49990,
        "original_price": 49990,
        "brand": "Lenovo",
    }


class TestAnalyzeProductDeals:
    def test_discount_deal(self, product_with_discount):
        deals = analyze_product_deals(product_with_discount)
        assert len(deals) > 0
        assert deals[0]["deal_type"] == "price_drop"
        assert deals[0]["savings"] == 10000

    def test_no_discount(self, product_without_discount):
        deals = analyze_product_deals(product_without_discount)
        assert len(deals) == 0

    def test_discount_percentage(self, product_with_discount):
        deals = analyze_product_deals(product_with_discount)
        assert deals[0]["discount_percentage"] == pytest.approx(10.0, rel=0.1)


class TestGenerateCouponSuggestions:
    def test_asus_coupons(self, product_with_discount):
        coupons = generate_coupon_suggestions(product_with_discount)
        assert len(coupons) > 0
        assert any("ASUS" in c.get("code", "") for c in coupons)

    def test_lenovo_coupons(self, product_without_discount):
        coupons = generate_coupon_suggestions(product_without_discount)
        assert len(coupons) > 0
        assert any("LENOVO" in c.get("code", "") for c in coupons)

    def test_unknown_brand(self):
        product = {"id": "3", "title": "Unknown", "brand": "UnknownBrand"}
        coupons = generate_coupon_suggestions(product)
        assert len(coupons) == 0
