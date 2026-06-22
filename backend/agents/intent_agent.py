import re
from typing import Any


async def extract_intent(state: dict[str, Any]) -> dict[str, Any]:
    query = state.get("user_query", "")

    intent = {
        "category": extract_category(query),
        "budget": extract_budget(query),
        "brands": extract_brands(query),
        "use_case": extract_use_case(query),
        "specifications": extract_specifications(query),
        "original_query": query,
    }

    return {"intent": intent}


def extract_category(query: str) -> str:
    categories = {
        "laptop": ["laptop", "notebook", "gaming laptop"],
        "headphone": ["headphone", "headphones", "earphone", "earbuds", "airpods"],
        "smartphone": ["phone", "smartphone", "mobile", "iphone", "galaxy"],
        "tablet": ["tablet", "ipad"],
        "camera": ["camera", "dslr", "mirrorless"],
        "monitor": ["monitor", "display"],
        "keyboard": ["keyboard"],
        "mouse": ["mouse"],
    }

    query_lower = query.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in query_lower:
                return category
    return "general"


def extract_budget(query: str) -> dict[str, int] | None:
    budget_patterns = [
        r"under\s*(?:₹|rs\.?|inr)?\s*([\d,]+)",
        r"below\s*(?:₹|rs\.?|inr)?\s*([\d,]+)",
        r"(?:₹|rs\.?|inr)\s*([\d,]+)\s*(?:or|and)\s*(?:less|below|under)",
        r"budget\s*(?:of|is|:)?\s*(?:₹|rs\.?|inr)?\s*([\d,]+)",
    ]

    for pattern in budget_patterns:
        match = re.search(pattern, query.lower())
        if match:
            amount = int(match.group(1).replace(",", ""))
            return {"min": 0, "max": amount}

    range_pattern = r"(?:₹|rs\.?|inr)\s*([\d,]+)\s*(?:to|-)\s*(?:₹|rs\.?|inr)?\s*([\d,]+)"
    range_match = re.search(range_pattern, query.lower())
    if range_match:
        min_amount = int(range_match.group(1).replace(",", ""))
        max_amount = int(range_match.group(2).replace(",", ""))
        return {"min": min_amount, "max": max_amount}

    return None


def extract_brands(query: str) -> list[str]:
    known_brands = [
        "apple", "samsung", "oneplus", "xiaomi", "realme", "vivo", "oppo",
        "asus", "lenovo", "hp", "dell", "acer", "msi", "razer",
        "sony", "jbl", "bose", "sennheiser",
        "canon", "nikon", "sony",
    ]

    query_lower = query.lower()
    found_brands = []
    for brand in known_brands:
        if brand in query_lower:
            found_brands.append(brand.capitalize())
    return found_brands


def extract_use_case(query: str) -> str:
    use_cases = {
        "gaming": ["gaming", "games", "gamer"],
        "programming": ["programming", "coding", "developer", "development"],
        "video editing": ["video editing", "video editor", "editing"],
        "photo editing": ["photo editing", "photo editor", "photoshop"],
        "office": ["office", "work", "business", "productivity"],
        "student": ["student", "study", "college", "university"],
        "casual": ["casual", "everyday", "daily use"],
        "photography": ["photography", "camera", "photos"],
    }

    query_lower = query.lower()
    for use_case, keywords in use_cases.items():
        for keyword in keywords:
            if keyword in query_lower:
                return use_case
    return "general"


def extract_specifications(query: str) -> dict[str, Any]:
    specs = {}

    ram_match = re.search(r"(\d+)\s*gb\s*ram", query.lower())
    if ram_match:
        specs["ram"] = f"{ram_match.group(1)}GB"

    storage_match = re.search(r"(\d+)\s*(?:gb|tb)\s*(?:ssd|hdd|storage)", query.lower())
    if storage_match:
        specs["storage"] = storage_match.group(0)

    return specs
