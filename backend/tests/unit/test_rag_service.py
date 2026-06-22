import pytest
from unittest.mock import MagicMock


class TestRAGServiceTools:
    def test_products_collection_created(self):
        from mcp_servers.product_server import product_server
        assert "search_products" in product_server.tools
        assert "get_product_details" in product_server.tools
        assert "compare_products" in product_server.tools
        assert "recommend_products" in product_server.tools

    def test_review_server_tools(self):
        from mcp_servers.review_server import review_server
        assert "fetch_reviews" in review_server.tools
        assert "summarize_reviews" in review_server.tools
        assert "analyze_sentiment" in review_server.tools

    def test_analyze_sentiment_positive(self):
        from mcp_servers.review_server import analyze_sentiment
        import asyncio
        result = asyncio.run(analyze_sentiment("This product is excellent and amazing!"))
        assert result["sentiment_score"] > 0
        assert result["label"] == "positive"

    def test_analyze_sentiment_negative(self):
        from mcp_servers.review_server import analyze_sentiment
        import asyncio
        result = asyncio.run(analyze_sentiment("This is terrible and broken. Worst product ever."))
        assert result["sentiment_score"] < 0
        assert result["label"] == "negative"

    def test_analyze_sentiment_neutral(self):
        from mcp_servers.review_server import analyze_sentiment
        import asyncio
        result = asyncio.run(analyze_sentiment("The product is okay."))
        assert result["label"] == "neutral"
