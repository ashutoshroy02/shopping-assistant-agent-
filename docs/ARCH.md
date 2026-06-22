# Architecture Document

## System Overview

The AI Shopping Assistant Platform is a multi-agent system that orchestrates specialized AI agents to research products, compare alternatives, analyze reviews, and generate personalized recommendations.

## System Diagram

```mermaid
graph TD
    Client[Next.js Frontend] --> API[FastAPI Backend]
    API --> Auth[Auth Service]
    API --> Graph[LangGraph Orchestrator]
    
    Graph --> IntentAgent[Intent Agent]
    Graph --> SearchAgent[Search Agent]
    Graph --> ReviewAgent[Review Agent]
    Graph --> ComparisonAgent[Comparison Agent]
    Graph --> RecommendAgent[Recommendation Agent]
    Graph --> DealAgent[Deal Agent]
    Graph --> PriceAgent[Price Agent]
    Graph --> ReflectAgent[Reflection Agent]
    
    SearchAgent --> ProductMCP[Product MCP Server]
    ReviewAgent --> ReviewMCP[Review MCP Server]
    PriceAgent --> PricingMCP[Pricing MCP Server]
    DealAgent --> DealsMCP[Deals MCP Server]
    
    ProductMCP --> DB[(PostgreSQL)]
    ReviewMCP --> DB
    PricingMCP --> DB
    DealsMCP --> DB
    
    Graph --> Redis[(Redis Cache)]
    Graph --> ChromaDB[(ChromaDB Vector Store)]
    
    API --> WebSocket[WebSocket Server]
    WebSocket --> Client
```

## Component Responsibilities

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| Frontend | UI, chat interface, dashboards | Next.js, TypeScript, Tailwind |
| API Layer | Request routing, auth, validation | FastAPI, Pydantic |
| LangGraph | Agent orchestration, workflow control | LangGraph, StateGraph |
| MCP Servers | Tool exposure, data access | FastMCP, Python |
| Database | Persistent storage | PostgreSQL |
| Cache | Session data, rate limiting | Redis |
| Vector Store | Semantic search, RAG | ChromaDB |

## Critical User Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Graph
    participant Agents
    participant MCP
    participant DB

    User->>Frontend: Enter query
    Frontend->>API: POST /chat
    API->>Graph: Initialize workflow
    
    Graph->>Agents: Intent Agent
    Agents->>DB: Extract parameters
    
    Graph->>Agents: Search Agent
    Agents->>MCP: search_products()
    MCP->>DB: Query products
    MCP-->>Agents: Product list
    
    Graph->>Agents: Review Agent
    Agents->>MCP: fetch_reviews()
    MCP->>DB: Query reviews
    MCP-->>Agents: Review data
    
    Graph->>Agents: Comparison Agent
    Agents-->>Graph: Comparison results
    
    Graph->>Agents: Recommendation Agent
    Agents-->>Graph: Ranked products
    
    Graph->>Agents: Reflection Agent
    Agents-->>Graph: Validation passed
    
    Graph-->>API: Final results
    API-->>Frontend: Response
    Frontend-->>User: Display recommendations
```

## Data Model Overview

```mermaid
erDiagram
    USERS ||--o{ RECOMMENDATIONS : receives
    USERS ||--o{ SAVED_PRODUCTS : saves
    USERS ||--o{ SEARCH_HISTORY : searches
    
    PRODUCTS ||--o{ REVIEWS : has
    PRODUCTS ||--o{ PRICE_HISTORY : tracks
    PRODUCTS ||--o{ RECOMMENDATIONS : recommends
    PRODUCTS ||--o{ SAVED_PRODUCTS : saved_in
    
    USERS {
        uuid id PK
        string name
        string email
        string password_hash
        timestamp created_at
    }
    
    PRODUCTS {
        uuid id PK
        string title
        decimal price
        float rating
        string category
        string brand
        jsonb specifications
        timestamp created_at
    }
    
    REVIEWS {
        uuid id PK
        uuid product_id FK
        text review_text
        float rating
        float sentiment_score
        jsonb metadata
        timestamp created_at
    }
    
    RECOMMENDATIONS {
        uuid id PK
        uuid user_id FK
        uuid product_id FK
        float score
        jsonb reasoning
        timestamp created_at
    }
    
    PRICE_HISTORY {
        uuid id PK
        uuid product_id FK
        decimal price
        string source
        timestamp recorded_at
    }
```

## Deployment Topology

| Service | Platform | Configuration |
|---------|----------|---------------|
| Frontend | Vercel/Railway | Next.js build |
| Backend | AWS ECS/Railway | FastAPI + Uvicorn |
| PostgreSQL | AWS RLS/Supabase | Managed DB |
| Redis | AWS ElastiCache/Upstash | Managed cache |
| ChromaDB | Self-hosted | Docker container |

## External Dependencies

| Dependency | Purpose | Fallback |
|------------|---------|----------|
| OpenAI/Anthropic API | LLM inference | Rate-limited queue |
| Amazon API | Product search | Mock data |
| Flipkart API | Product search | Mock data |
| Google OAuth | Authentication | Email/password only |

## Failure Modes & Mitigations

| Failure | Impact | Mitigation |
|---------|--------|------------|
| LLM API down | Agents fail | Fallback responses, retry queue |
| MCP server timeout | Tool calls fail | Timeout + cached responses |
| Database connection lost | Data persistence fails | Connection pooling, retry logic |
| Redis unavailable | Cache miss | Direct DB queries |
| ChromaDB unavailable | RAG fails | Keyword search fallback |

## Security Considerations

1. **Authentication**: JWT with refresh tokens, Google OAuth
2. **Authorization**: Role-based access control (User, Admin)
3. **Input Validation**: Pydantic models, SQL injection prevention
4. **Rate Limiting**: Redis-backed rate limiting per user
5. **Secrets**: Environment variables, never committed
6. **CORS**: Restricted to frontend domain
7. **HTTPS**: Enforced in production

## Scalability Notes

**Current targets**: 1000 concurrent users, 10k products
**Bottlenecks at scale**: 
- LLM API rate limits → Queue system, batch processing
- Database queries → Connection pooling, read replicas
- Vector search → ChromaDB sharding, FAISS for large datasets

**Intentional simplifications**:
- Single-region deployment (can expand later)
- In-memory caching (can add distributed cache)
- Synchronous MCP calls (can add async workers)
