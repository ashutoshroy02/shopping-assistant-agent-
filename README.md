# AI Shopping Assistant

Multi-Agent Shopping Assistant with LLM-powered recommendations. Ask questions in natural language and get personalized product suggestions.

## Features

- **Natural Language Shopping** - "Find gaming laptops under ₹1,00,000"
- **Multi-Agent Pipeline** - 8 LangGraph agents: intent → search → reviews → compare → recommend → deals → price → reflect
- **LLM-Powered Responses** - OpenRouter integration for natural conversational replies
- **Fast Generic Queries** - Instant template responses for simple queries like "hi"
- **Review Intelligence** - Sentiment analysis, pros/cons extraction
- **Product Comparison** - Side-by-side feature comparison
- **Price Tracking** - Historical data, price drop predictions
- **Deal Discovery** - Coupons, discounts, cashback offers
- **No Auth Required** - Chat directly, no sign-up needed

## Architecture

```
Streamlit Frontend (:8501)
        │
        ▼
FastAPI Backend (:8000)
        │
        ▼
LangGraph Orchestrator
  Intent → Search → Reviews → Compare → Recommend → Deals → Price → Reflect
        │
        ▼
SQLite (data) + OpenRouter LLM
```

## Quick Start

### Prerequisites

- Python 3.11+
- Git

### 1. Clone & Setup

```bash
git clone https://github.com/ashutoshroy02/shopping-assistant-agent-.git
cd shopping-assistant-agent-
```

### 2. Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
GROQ_API_KEY=sk-or-v1-your-openrouter-key
GROQ_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=google/gemma-4-26b-a4b-it:free
```

### 3. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate  # Linux/Mac

pip install fastapi uvicorn sqlalchemy aiosqlite alembic pydantic pydantic-settings python-jose[cryptography] bcrypt python-multipart httpx tenacity structlog langgraph langchain-core openai email-validator streamlit

python -m database.seed
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

### 4. Frontend

```bash
cd backend
streamlit run app.py --server.port 8501
```

Open http://localhost:8501

## Project Structure

```
backend/
├── agents/                  # LangGraph AI agents
│   ├── intent_agent.py      # Regex-based intent extraction
│   ├── search_agent.py      # DB product search with fallback
│   ├── review_agent.py      # Sentiment analysis
│   ├── comparison_agent.py  # Feature comparison
│   ├── recommendation_agent.py  # Scoring + template reasoning
│   ├── deal_agent.py        # Discount/coupon finder
│   ├── price_agent.py       # Price tracking
│   └── reflection_agent.py  # Validation + LLM final response
├── graph/
│   ├── state.py             # Agent state schema
│   └── workflow.py          # LangGraph pipeline
├── api/routes/
│   └── chat.py              # Chat endpoint (no auth)
├── database/
│   ├── connection.py        # SQLite auto-fallback
│   ├── models.py            # SQLAlchemy models
│   └── seed.py              # Seed data (5 products, 2 users)
├── services/
│   ├── llm.py               # OpenRouter LLM client
│   ├── auth.py              # JWT auth (optional)
│   └── memory.py            # In-memory fallback (no Redis)
├── app.py                   # Streamlit frontend
├── config.py                # Settings from .env
└── requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat` | Send message, get AI response |
| GET | `/api/v1/products` | List all products |
| GET | `/api/v1/products/categories` | List categories |
| POST | `/api/v1/products/recommend` | Get recommendations |
| POST | `/api/v1/products/compare` | Compare products |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger API docs |

## How It Works

1. **Intent Agent** - Extracts category, budget, use case from query via regex
2. **Search Agent** - Queries SQLite, falls back to top-rated products for generic queries
3. **Review Agent** - Analyzes sentiment (keyword-based or LLM)
4. **Comparison Agent** - Side-by-side feature comparison
5. **Recommendation Agent** - Scores products algorithmically (rating, budget fit, use case match)
6. **Deal Agent** - Finds discounts, coupons, cashback
7. **Price Agent** - Historical price analysis
8. **Reflection Agent** - Validates output, generates final response:
   - Generic query → instant template (~200ms)
   - Specific query → LLM-powered natural response (~8-10s)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | OpenRouter API key | - |
| `GROQ_BASE_URL` | API base URL | `https://openrouter.ai/api/v1` |
| `LLM_MODEL` | Model ID | `google/gemma-4-26b-a4b-it:free` |
| `DATABASE_URL` | Database connection | SQLite fallback |
| `SECRET_KEY` | JWT secret | dev key |

## Tech Stack

- **Backend**: FastAPI + LangGraph + SQLAlchemy
- **Frontend**: Streamlit
- **Database**: SQLite (PostgreSQL optional)
- **LLM**: OpenRouter (free models)
- **No external services required** - runs fully local

## License

MIT
