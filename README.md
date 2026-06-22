# 🛒 AI Shopping Assistant

A production-grade Multi-Agent Shopping Assistant capable of autonomously researching products, comparing alternatives, analyzing reviews, tracking prices, discovering deals, and generating personalized recommendations.

## 🎯 Features

- **Natural Language Shopping** - Ask questions like "Find gaming laptops under ₹1,00,000"
- **Multi-Agent Architecture** - 8 specialized AI agents working together
- **Review Intelligence** - Sentiment analysis, pros/cons extraction
- **Product Comparison** - Side-by-side feature comparison
- **Price Tracking** - Historical data, price drop predictions
- **Deal Discovery** - Coupons, discounts, cashback offers
- **Personalized Recommendations** - Based on your preferences and budget
- **RAG Knowledge Base** - Semantic search across product data

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Next.js Frontend                         │
│  Chat Interface │ Products │ Analytics │ Price Tracker      │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  Auth │ Chat │ Products │ Analytics │ Research               │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  LangGraph Orchestrator                      │
│  Intent → Search → Reviews → Compare → Recommend → Reflect  │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     MCP Servers                              │
│  Product │ Review │ Pricing │ Deals                          │
└─────────────────────────────┬───────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌──────────┐       ┌──────────┐       ┌──────────┐
    │PostgreSQL│       │  Redis   │       │ ChromaDB │
    │  (Data)  │       │ (Cache)  │       │  (RAG)   │
    └──────────┘       └──────────┘       └──────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/shopping-assistant.git
cd shopping-assistant
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start Services

```bash
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- ChromaDB (port 8000)

### 4. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Seed database
python -m database.seed

# Start server
uvicorn api.main:app --reload
```

Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

### 5. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: http://localhost:3000

## 📁 Project Structure

```
shopping-assistant/
├── backend/
│   ├── agents/              # LangGraph AI agents
│   │   ├── intent_agent.py      # Extracts query parameters
│   │   ├── search_agent.py      # Product discovery
│   │   ├── review_agent.py      # Sentiment analysis
│   │   ├── comparison_agent.py  # Side-by-side comparison
│   │   ├── recommendation_agent.py # Ranking & scoring
│   │   ├── deal_agent.py        # Coupon & discount finder
│   │   ├── price_agent.py       # Price tracking & predictions
│   │   └── reflection_agent.py  # Quality validation
│   ├── graph/               # LangGraph workflow
│   │   ├── state.py             # State schema
│   │   └── workflow.py          # Agent orchestration
│   ├── mcp_servers/         # Model Context Protocol servers
│   │   ├── product_server.py    # Product tools
│   │   ├── review_server.py     # Review tools
│   │   ├── pricing_server.py    # Pricing tools
│   │   └── deals_server.py      # Deals tools
│   ├── api/                 # FastAPI routes
│   │   ├── main.py              # App entry point
│   │   ├── routes/              # API endpoints
│   │   └── middleware/          # CORS, auth, rate limiting
│   ├── database/            # SQLAlchemy models & migrations
│   ├── services/            # Business logic
│   │   ├── auth.py              # JWT authentication
│   │   ├── rag.py               # ChromaDB vector search
│   │   └── memory.py            # Redis session memory
│   ├── tests/               # Test suite
│   │   ├── api/                 # API endpoint tests
│   │   ├── unit/                # Unit tests
│   │   └── integration/         # Integration tests
│   ├── config.py            # Settings management
│   ├── pyproject.toml       # Python project config
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Backend Docker image
│   └── alembic.ini          # Database migration config
├── frontend/
│   ├── app/                 # Next.js pages
│   │   ├── page.tsx            # Home page
│   │   ├── chat/               # Chat interface
│   │   ├── products/           # Product browser
│   │   ├── saved/              # Wishlist
│   │   ├── tracker/            # Price tracker
│   │   └── analytics/          # Analytics dashboard
│   ├── components/          # React components
│   │   ├── ui/                 # Shadcn UI components
│   │   ├── chat/               # Chat components
│   │   └── products/           # Product components
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utilities & API client
│   ├── types/               # TypeScript types
│   ├── package.json         # Node dependencies
│   └── tailwind.config.js   # Tailwind CSS config
├── docs/                    # Documentation
│   ├── ARCH.md              # Architecture diagrams
│   ├── API.md               # API specification
│   ├── DB.md                # Database schema
│   ├── FLOW.md              # User journeys
│   ├── PRD.md               # Product requirements
│   └── IMPL-PLAN.md         # Implementation plan
├── docker-compose.yml       # Docker services
├── .env.example             # Environment template
└── AGENTS.md                # AI agent configuration
```

## 🔧 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Create account |
| POST | `/api/v1/auth/login` | Get access token |
| POST | `/api/v1/auth/refresh` | Refresh token |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat` | Send message to AI |
| GET | `/api/v1/chat/sessions` | List chat sessions |
| GET | `/api/v1/chat/history/{id}` | Get chat history |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/products` | List products |
| GET | `/api/v1/products/{id}` | Get product details |
| GET | `/api/v1/products/categories` | List categories |
| GET | `/api/v1/products/brands` | List brands |
| POST | `/api/v1/products/recommend` | Get recommendations |
| POST | `/api/v1/products/compare` | Compare products |
| GET | `/api/v1/products/price-history/{id}` | Price history |

### Saved Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/saved` | List saved products |
| POST | `/api/v1/saved/{id}` | Save product |
| DELETE | `/api/v1/saved/{id}` | Remove from saved |

### Price Tracking
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/products/tracked` | List tracked products |
| POST | `/api/v1/products/track-price` | Start tracking |
| DELETE | `/api/v1/products/track-price/{id}` | Stop tracking |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/analytics` | Get analytics |
| GET | `/api/v1/analytics/trends` | Search trends |

### Research
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/research` | Start autonomous research |

## 🧪 Testing

### Run All Tests

```bash
# Backend tests
cd backend
pytest -v

# With coverage
pytest --cov=backend --cov-report=html

# Frontend tests
cd frontend
npm test
```

### Test Structure

```
backend/tests/
├── api/                    # API endpoint tests
│   ├── test_auth.py           # Authentication tests
│   ├── test_chat.py           # Chat endpoint tests
│   └── test_products.py       # Product endpoint tests
├── unit/                   # Unit tests
│   ├── test_agents.py         # Agent logic tests
│   └── test_services.py       # Service tests
└── integration/            # Integration tests
    ├── test_workflow.py       # LangGraph workflow tests
    └── test_mcp.py            # MCP server tests
```

### Test Coverage

We aim for **80%+ code coverage**. Check coverage:

```bash
pytest --cov=backend --cov-report=term-missing
```

## 🔐 Environment Variables

```env
# Application
APP_NAME=Shopping Assistant
APP_ENV=development
DEBUG=true

# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=shopping_assistant
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/shopping_assistant

# Redis
REDIS_URL=redis://localhost:6379/0

# ChromaDB
CHROMA_HOST=localhost
CHROMA_PORT=8000

# LLM (choose one)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild services
docker-compose build --no-cache

# Run backend in container
docker-compose up backend
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/ARCH.md) | System design & diagrams |
| [API Specification](docs/API.md) | Endpoint contracts |
| [Database Schema](docs/DB.md) | Data model & ERD |
| [User Flows](docs/FLOW.md) | User journeys |
| [PRD](docs/PRD.md) | Product requirements |
| [Implementation Plan](docs/IMPL-PLAN.md) | Build phases |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Convention

```
feat:     New feature
fix:      Bug fix
docs:     Documentation
style:    Formatting
refactor: Code restructuring
test:     Adding tests
chore:    Maintenance
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Next.js](https://nextjs.org/) - Frontend framework
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Shadcn UI](https://ui.shadcn.com/) - UI components
