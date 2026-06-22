# API Specification

**Base URL**: `http://localhost:8000/api/v1`

**Authentication**: Bearer token (JWT) in Authorization header

---

## Authentication Endpoints

### POST /auth/register
Register a new user.

**Request**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### POST /auth/login
Authenticate user and get tokens.

**Request**:
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response** (200):
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### POST /auth/refresh
Refresh access token.

**Request**:
```json
{
  "refresh_token": "eyJ..."
}
```

**Response** (200):
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

## Chat Endpoints

### POST /chat
Send message to shopping assistant.

**Request**:
```json
{
  "message": "Find the best gaming laptop under 100000",
  "session_id": "optional-session-id",
  "context": {
    "budget": 100000,
    "category": "laptops"
  }
}
```

**Response** (200):
```json
{
  "response": "I found 5 gaming laptops under ₹1,00,000...",
  "session_id": "uuid",
  "products": [
    {
      "id": "uuid",
      "title": "ASUS ROG Strix G15",
      "price": 89990,
      "rating": 4.5,
      "image_url": "https://...",
      "reasoning": "Best value for money with RTX 3060..."
    }
  ],
  "metadata": {
    "agents_used": ["intent", "search", "recommendation"],
    "processing_time_ms": 2340
  }
}
```

### GET /chat/history/{session_id}
Get chat history for session.

**Response** (200):
```json
{
  "session_id": "uuid",
  "messages": [
    {
      "role": "user",
      "content": "Find gaming laptops",
      "timestamp": "2024-01-01T00:00:00Z"
    },
    {
      "role": "assistant",
      "content": "I found 5 options...",
      "timestamp": "2024-01-01T00:00:05Z"
    }
  ]
}
```

---

## Product Endpoints

### POST /recommend
Get personalized product recommendations.

**Request**:
```json
{
  "category": "laptops",
  "budget": {
    "min": 50000,
    "max": 100000
  },
  "preferences": {
    "brands": ["ASUS", "MSI"],
    "features": ["gaming", "high-performance"]
  },
  "limit": 10
}
```

**Response** (200):
```json
{
  "recommendations": [
    {
      "product_id": "uuid",
      "title": "ASUS ROG Strix G15",
      "price": 89990,
      "rating": 4.5,
      "score": 0.92,
      "reasoning": "Best overall value...",
      "pros": ["Great performance", "Good battery"],
      "cons": ["Heavy", "Fan noise"]
    }
  ],
  "categories": {
    "best_overall": "uuid",
    "budget_pick": "uuid",
    "premium_choice": "uuid"
  }
}
```

### POST /compare
Compare multiple products side-by-side.

**Request**:
```json
{
  "product_ids": ["uuid1", "uuid2", "uuid3"]
}
```

**Response** (200):
```json
{
  "comparison": {
    "products": [
      {
        "id": "uuid1",
        "title": "ASUS ROG Strix G15",
        "price": 89990,
        "rating": 4.5,
        "specifications": {
          "ram": "16GB",
          "storage": "512GB SSD",
          "gpu": "RTX 3060"
        }
      }
    ],
    "analysis": {
      "winner": "uuid1",
      "reasoning": "Best value for money...",
      "category_scores": {
        "performance": {"uuid1": 9, "uuid2": 8},
        "battery": {"uuid1": 7, "uuid2": 9}
      }
    }
  }
}
```

### GET /products/{product_id}
Get detailed product information.

**Response** (200):
```json
{
  "id": "uuid",
  "title": "ASUS ROG Strix G15",
  "price": 89990,
  "original_price": 99990,
  "rating": 4.5,
  "review_count": 1250,
  "category": "gaming-laptops",
  "brand": "ASUS",
  "specifications": {},
  "images": ["https://..."],
  "availability": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## Price Tracking Endpoints

### POST /track-price
Start tracking a product's price.

**Request**:
```json
{
  "product_id": "uuid",
  "target_price": 80000,
  "alert_on_drop": true
}
```

**Response** (201):
```json
{
  "tracking_id": "uuid",
  "product_id": "uuid",
  "target_price": 80000,
  "current_price": 89990,
  "status": "active"
}
```

### GET /price-history/{product_id}
Get price history for a product.

**Query Parameters**:
- `period`: 7d, 30d, 90d, 1y
- `source`: all, amazon, flipkart

**Response** (200):
```json
{
  "product_id": "uuid",
  "history": [
    {
      "price": 89990,
      "source": "amazon",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  ],
  "statistics": {
    "current": 89990,
    "lowest": 79990,
    "highest": 99990,
    "average": 89990,
    "trend": "stable"
  },
  "prediction": {
    "next_sale_date": "2024-02-01",
    "predicted_price": 79990,
    "confidence": 0.85
  }
}
```

---

## Autonomous Research Endpoints

### POST /autonomous-research
Start autonomous shopping research.

**Request**:
```json
{
  "query": "Find the best gaming laptop under 1 lakh",
  "options": {
    "max_products": 20,
    "include_deals": true,
    "include_price_forecast": true,
    "detailed_reviews": true
  }
}
```

**Response** (200):
```json
{
  "research_id": "uuid",
  "status": "completed",
  "report": {
    "summary": "Based on comprehensive research...",
    "top_picks": [...],
    "comparison_table": {...},
    "price_insights": {...},
    "deals_found": [...],
    "recommendations": {
      "best_overall": {...},
      "budget_pick": {...},
      "premium_choice": {...}
    }
  },
  "metadata": {
    "products_analyzed": 15,
    "reviews_processed": 2500,
    "processing_time_ms": 8500
  }
}
```

---

## Analytics Endpoints

### GET /analytics
Get user and platform analytics.

**Query Parameters**:
- `period`: 7d, 30d, 90d
- `type`: user, platform, all

**Response** (200):
```json
{
  "user_analytics": {
    "total_searches": 45,
    "saved_products": 12,
    "categories_viewed": ["laptops", "phones"],
    "average_budget": 75000
  },
  "platform_analytics": {
    "total_users": 1000,
    "active_users": 250,
    "popular_categories": [...],
    "recommendation_accuracy": 0.89
  }
}
```

---

## Error Responses

All endpoints return errors in consistent format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

**Error Codes**:
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (resource doesn't exist)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error

---

## Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| /auth/* | 10 requests | 1 minute |
| /chat | 30 requests | 1 minute |
| /recommend | 20 requests | 1 minute |
| /compare | 20 requests | 1 minute |
| /track-price | 10 requests | 1 minute |
| /autonomous-research | 5 requests | 1 minute |
| /analytics | 60 requests | 1 minute |
