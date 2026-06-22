# AI Shopping Assistant Platform

**Tech Stack:** Python, LangGraph, MCP (Model Context Protocol), FastAPI, PostgreSQL, Redis, ChromaDB, Next.js, TypeScript, Docker

**Duration:** Sep 2024 – Dec 2024

---

# Project Overview

Build a production-grade Multi-Agent Shopping Assistant capable of autonomously researching products, comparing alternatives, analyzing reviews, tracking prices, discovering deals, and generating personalized recommendations.

The system uses LangGraph to orchestrate multiple AI agents and MCP servers to expose shopping tools. It supports conversational interactions, autonomous research workflows, long-term memory, vector search, and self-reflection mechanisms to improve recommendation quality.

---

# Key Features

## Intelligent Product Discovery

- Natural language shopping queries
- Multi-platform product search
- Budget-aware recommendations
- Personalized suggestions
- Brand preference understanding
- Product filtering and ranking

### Example Queries

- Find the best gaming laptop under ₹1,00,000
- Recommend a DSLR camera for beginners
- Compare iPhone 15 and Samsung S24
- Best monitor for programming under ₹20,000

---

## Multi-Agent Architecture

The platform consists of specialized AI agents working together.

### User Intent Agent

Extracts:

- Product category
- Budget
- Preferred brands
- Desired specifications
- Use case

### Product Search Agent

Searches across:

- Amazon
- Flipkart
- Walmart
- BestBuy
- Product APIs

### Review Analysis Agent

Analyzes:

- Product reviews
- User sentiment
- Common complaints
- Positive feedback
- Review quality

### Comparison Agent

Compares:

- Features
- Pricing
- Ratings
- Reviews
- Specifications

### Recommendation Agent

Ranks products based on:

- Budget
- Features
- Reviews
- Ratings
- User preferences

### Deal Finder Agent

Discovers:

- Coupons
- Discount offers
- Cashback opportunities
- Promotional campaigns

### Price Tracking Agent

Tracks:

- Historical prices
- Discount periods
- Price drops
- Price predictions

### Reflection Agent

Performs:

- Output validation
- Recommendation review
- Hallucination detection
- Missing information detection
- Automatic retries

---

# LangGraph Workflow

```text
User Query
      │
      ▼
Intent Agent
      │
      ▼
Product Search Agent
      │
      ▼
Review Analysis Agent
      │
      ▼
Comparison Agent
      │
      ▼
Recommendation Agent
      │
      ▼
Reflection Agent
      │
 ┌────┴────┐
 │         │
Retry    Final Output
```

---

# MCP Servers

## Product MCP Server

### Tools

```python
search_products()
get_product_details()
compare_products()
recommend_products()
```

---

## Review MCP Server

### Tools

```python
fetch_reviews()
summarize_reviews()
analyze_sentiment()
```

---

## Pricing MCP Server

### Tools

```python
track_price()
get_price_history()
predict_price_drop()
```

---

## Deals MCP Server

### Tools

```python
find_discounts()
find_coupons()
get_cashback_offers()
```

---

# RAG Shopping Knowledge Base

Vector Database:

- ChromaDB
- FAISS

Stores:

- Product specifications
- Product manuals
- FAQs
- Brand information
- User guides
- Shopping policies

Capabilities:

- Semantic search
- Product question answering
- Context-aware recommendations

---

# Conversational Memory

Stores:

- Previous searches
- Favorite brands
- Preferred categories
- Budget history
- Saved products

Enables:

- Personalized recommendations
- Context retention
- Multi-session continuity

---

# Autonomous Shopping Research Mode

User provides a high-level task.

Example:

```text
Find the best gaming laptop under ₹1 lakh.
```

System automatically:

1. Searches products
2. Fetches reviews
3. Compares alternatives
4. Evaluates value for money
5. Finds deals
6. Generates final report

No further user interaction required.

---

# Review Intelligence Engine

Extracts:

## Pros

- Performance
- Battery life
- Build quality
- Camera quality

## Cons

- Heating issues
- Poor customer support
- Software bugs
- Durability concerns

## Sentiment Score

Example:

```json
{
  "sentiment": 0.91,
  "positive": 87,
  "negative": 13
}
```

---

# Product Comparison Engine

Generates side-by-side comparisons.

| Feature | Product A | Product B |
|----------|-----------|-----------|
| Price | ₹85,000 | ₹89,000 |
| Rating | 4.5 | 4.6 |
| Battery | 8 Hours | 10 Hours |
| RAM | 16GB | 16GB |
| Storage | 512GB | 1TB |

---

# Recommendation Engine

Uses:

- LLM scoring
- User preferences
- Ratings
- Reviews
- Product popularity
- Value-for-money score

Outputs:

## Best Overall

Most balanced recommendation.

## Budget Pick

Best value option.

## Premium Choice

Highest-end recommendation.

---

# Price Intelligence

Features:

- Historical price graphs
- Discount tracking
- Sale predictions
- Price drop alerts

Data Sources:

- Marketplace APIs
- Product feeds
- Cached historical data

---

# Analytics Dashboard

Displays:

## User Analytics

- Search trends
- Favorite categories
- Saved products

## Product Analytics

- Popular products
- Highest-rated items
- Trending categories

## Business Analytics

- Recommendation accuracy
- Conversion metrics
- Agent performance

---

# Authentication System

Supports:

- JWT Authentication
- Google OAuth
- Role-Based Access Control

Roles:

- User
- Admin

---

# Database Design

## Users

```sql
id
name
email
password_hash
created_at
```

## Products

```sql
id
title
price
rating
category
brand
```

## Reviews

```sql
id
product_id
review_text
rating
sentiment_score
```

## Recommendations

```sql
id
user_id
product_id
recommendation_score
```

## Price History

```sql
id
product_id
price
timestamp
```

---

# API Endpoints

## Chat

```http
POST /chat
```

## Product Recommendations

```http
POST /recommend
```

## Product Comparison

```http
POST /compare
```

## Price Tracking

```http
POST /track-price
```

## Price History

```http
GET /price-history
```

## Autonomous Research

```http
POST /autonomous-research
```

## Analytics

```http
GET /analytics
```

---

# Frontend Features

Built with:

- Next.js
- TypeScript
- TailwindCSS
- Shadcn UI

Pages:

## Chat Interface

Interactive shopping assistant.

## Product Dashboard

Browse and compare products.

## Analytics Dashboard

View recommendations and insights.

## Saved Products

Wishlist management.

## Price Tracker

Monitor product pricing.

---

# Deployment

Containerized using Docker.

Services:

```yaml
frontend
backend
postgres
redis
chromadb
```

Deployment Targets:

- AWS
- Azure
- Railway
- Render
- GCP

---

# Testing

Includes:

- Unit Tests
- Integration Tests
- MCP Tool Tests
- LangGraph Workflow Tests
- API Tests

Coverage Target:

```text
80%+
```

---

# Folder Structure

```text
shopping-assistant/
│
├── backend/
│   ├── agents/
│   ├── graph/
│   ├── mcp_servers/
│   ├── api/
│   ├── database/
│   ├── services/
│   └── tests/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   └── lib/
│
├── chromadb/
├── docker/
├── docs/
├── docker-compose.yml
└── README.md
```

---

# Resume Description

### AI Shopping Assistant Platform | Python, LangGraph, MCP, FastAPI, PostgreSQL, ChromaDB

**Sep 2024 – Dec 2024**

- Designed and developed a multi-agent AI shopping assistant using LangGraph and MCP, orchestrating specialized agents for product discovery, review intelligence, comparison, pricing analysis, and recommendation workflows.
- Built autonomous shopping research capabilities with self-reflection and retry mechanisms, improving recommendation reliability and decision quality.
- Implemented FastAPI microservices, PostgreSQL persistence, Redis caching, and ChromaDB-powered RAG pipelines for context-aware product recommendations.
- Developed conversational shopping copilots capable of multi-step reasoning, sentiment-driven review analysis, deal discovery, and personalized product ranking.
- Containerized the platform using Docker and deployed scalable services supporting real-time product intelligence and analytics dashboards.