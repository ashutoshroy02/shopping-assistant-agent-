import pytest
from mcp_servers.product_server import product_server
from mcp_servers.review_server import review_server
from mcp_servers.pricing_server import pricing_server
from mcp_servers.deals_server import deals_server


class TestProductServer:
    def test_server_exists(self):
        assert product_server is not None
        assert product_server.name == "product"

    def test_has_tools(self):
        assert len(product_server.tools) > 0

    def test_tools_listed(self):
        tools = product_server.get_tools_schema()
        tool_names = [t["name"] for t in tools]
        assert "search_products" in tool_names
        assert "get_product_details" in tool_names
        assert "compare_products" in tool_names
        assert "recommend_products" in tool_names


class TestReviewServer:
    def test_server_exists(self):
        assert review_server is not None
        assert review_server.name == "review"

    def test_has_tools(self):
        assert len(review_server.tools) > 0

    def test_tools_listed(self):
        tools = review_server.get_tools_schema()
        tool_names = [t["name"] for t in tools]
        assert "fetch_reviews" in tool_names
        assert "summarize_reviews" in tool_names
        assert "analyze_sentiment" in tool_names


class TestPricingServer:
    def test_server_exists(self):
        assert pricing_server is not None
        assert pricing_server.name == "pricing"

    def test_has_tools(self):
        assert len(pricing_server.tools) > 0

    def test_tools_listed(self):
        tools = pricing_server.get_tools_schema()
        tool_names = [t["name"] for t in tools]
        assert "track_price" in tool_names
        assert "get_price_history" in tool_names
        assert "predict_price_drop" in tool_names


class TestDealsServer:
    def test_server_exists(self):
        assert deals_server is not None
        assert deals_server.name == "deals"

    def test_has_tools(self):
        assert len(deals_server.tools) > 0

    def test_tools_listed(self):
        tools = deals_server.get_tools_schema()
        tool_names = [t["name"] for t in tools]
        assert "find_discounts" in tool_names
        assert "find_coupons" in tool_names
        assert "get_cashback_offers" in tool_names
