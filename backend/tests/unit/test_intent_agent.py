import pytest
from agents.intent_agent import (
    extract_budget,
    extract_brands,
    extract_category,
    extract_specifications,
    extract_use_case,
)


class TestExtractCategory:
    def test_gaming_laptop(self):
        assert extract_category("Find gaming laptop under 1 lakh") == "laptop"

    def test_smartphone(self):
        assert extract_category("Best smartphone under 50000") == "smartphone"

    def test_iphone(self):
        assert extract_category("Compare iPhone 15 and Samsung S24") == "smartphone"

    def test_tablet(self):
        assert extract_category("Best iPad for students") == "tablet"

    def test_headphone(self):
        assert extract_category("Wireless headphones with good bass") == "headphone"

    def test_monitor(self):
        assert extract_category("4K monitor for programming") == "monitor"

    def test_general(self):
        assert extract_category("Find something good") == "general"


class TestExtractBudget:
    def test_under_amount(self):
        result = extract_budget("Find laptop under 100000")
        assert result == {"min": 0, "max": 100000}

    def test_under_with_currency(self):
        result = extract_budget("Find laptop under ₹80,000")
        assert result == {"min": 0, "max": 80000}

    def test_below_amount(self):
        result = extract_budget("Best phone below 50000")
        assert result == {"min": 0, "max": 50000}

    def test_budget_of(self):
        result = extract_budget("Budget of 60000")
        assert result == {"min": 0, "max": 60000}

    def test_no_budget(self):
        result = extract_budget("Find best laptop")
        assert result is None


class TestExtractBrands:
    def test_single_brand(self):
        result = extract_brands("Find ASUS laptop")
        assert "Asus" in result

    def test_multiple_brands(self):
        result = extract_brands("Compare Apple and Samsung phones")
        assert "Apple" in result
        assert "Samsung" in result

    def test_no_brands(self):
        result = extract_brands("Find best laptop")
        assert result == []


class TestExtractUseCase:
    def test_gaming(self):
        assert extract_use_case("Find gaming laptop") == "gaming"

    def test_programming(self):
        assert extract_use_case("Best laptop for coding") == "programming"

    def test_student(self):
        assert extract_use_case("Laptop for college student") == "student"

    def test_office(self):
        assert extract_use_case("Office work laptop") == "office"

    def test_general(self):
        assert extract_use_case("Find best laptop") == "general"


class TestExtractSpecifications:
    def test_ram(self):
        result = extract_specifications("Find laptop with 16GB RAM")
        assert result.get("ram") == "16GB"

    def test_storage(self):
        result = extract_specifications("Find laptop with 512GB SSD")
        assert result.get("storage") == "512gb ssd"

    def test_no_specs(self):
        result = extract_specifications("Find best laptop")
        assert result == {}
