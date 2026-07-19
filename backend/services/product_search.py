import json
import subprocess
import os
from typing import Any


async def search_products_online(query: str) -> list[dict[str, Any]]:
    """Search real products via TinyFish CLI."""
    try:
        npm_global = os.path.expanduser("~\\AppData\\Roaming\\npm")
        tinyfish_cmd = os.path.join(npm_global, "tinyfish.cmd")

        if not os.path.exists(tinyfish_cmd):
            return []

        result = subprocess.run(
            f'"{tinyfish_cmd}" search query "{query}"',
            capture_output=True,
            text=True,
            timeout=25,
            shell=True,
            env={**os.environ, "PATH": npm_global + ";" + os.environ.get("PATH", "")},
        )

        if result.returncode != 0:
            return []

        data = json.loads(result.stdout)
        results = data.get("results", [])

        products = []
        for r in results:
            snippet = r.get("snippet", "")
            title = r.get("title", "")
            url = r.get("url", "")
            site = r.get("site_name", "")

            if not snippet and not title:
                continue

            price = extract_price(snippet)
            rating = extract_rating(snippet)

            products.append({
                "id": url,
                "title": extract_product_title(snippet, title),
                "description": snippet[:200],
                "price": price,
                "original_price": None,
                "rating": rating,
                "review_count": 0,
                "category": "smartphones" if "phone" in query.lower() else "general",
                "brand": extract_brand(snippet),
                "specifications": {},
                "images": [],
                "availability": True,
                "source_url": url,
                "source_site": site,
            })

        return products

    except Exception:
        return []


def extract_price(text: str) -> float:
    """Extract price from snippet."""
    import re
    patterns = [
        r"₹([\d,]+)",
        r"Rs\.?\s*([\d,]+)",
        r"INR\s*([\d,]+)",
        r"under\s*([\d,]+)",
        r"below\s*([\d,]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1).replace(",", ""))
    return 0.0


def extract_rating(text: str) -> float:
    """Extract rating from snippet."""
    import re
    match = re.search(r"(\d\.?\d?)\s*/\s*5", text)
    if match:
        return float(match.group(1))
    match = re.search(r"(\d\.?\d?)\s*rating", text.lower())
    if match:
        return float(match.group(1))
    return 0.0


def extract_brand(text: str) -> str:
    """Extract brand from snippet."""
    brands = [
        "Samsung", "Apple", "OnePlus", "Xiaomi", "Redmi", "Realme",
        "Vivo", "Oppo", "Motorola", "Nokia", "Poco", "Infinix",
        "Lava", "Nothing", "iQOO", "Honor", "Tecno",
    ]
    text_lower = text.lower()
    for brand in brands:
        if brand.lower() in text_lower:
            return brand
    return ""


def extract_product_title(snippet: str, fallback_title: str) -> str:
    """Extract product name from snippet or title."""
    if "(" in snippet:
        return snippet.split("(")[0].strip()
    if " - " in snippet:
        return snippet.split(" - ")[0].strip()
    return fallback_title[:100] if fallback_title else snippet[:100]
