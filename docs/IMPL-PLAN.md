# Implementation Plan

## Phase 0: Foundation (Days 1-2)

**Goal**: Project scaffolding, database setup, authentication skeleton

### T0.1: Initialize Project Structure
**Complexity**: XS (<1 hour)
**Files**: Root directory

**Tasks**:
- [ ] Create backend/ directory with Python project structure
- [ ] Create frontend/ directory with Next.js setup
- [ ] Create docker/ directory with service configs
- [ ] Create docs/ directory with documentation
- [ ] Initialize git repository
- [ ] Create .gitignore

**Acceptance Criteria**:
- Directory structure exists
- Git repo initialized
- .gitignore covers Python, Node, Docker

---

### T0.2: Set Up Docker Compose
**Complexity**: S (2-4 hours)
**Files**: docker-compose.yml, docker/*.yml

**Tasks**:
- [ ] Create docker-compose.yml with services
- [ ] Configure PostgreSQL service (port 5432)
- [ ] Configure Redis service (port 6379)
- [ ] Configure ChromaDB service (port 8000)
- [ ] Create .env.example with required variables
- [ ] Test all services start successfully

**Acceptance Criteria**:
- `docker-compose up` starts all services
- Services are accessible on their ports
- Health checks pass

---

### T0.3: Configure Python Backend
**Complexity**: M (1-2 days)
**Files**: backend/pyproject.toml, backend/*.py

**Tasks**:
- [ ] Create pyproject.toml with dependencies
- [ ] Set up FastAPI application structure
- [ ] Configure environment variables loading
- [ ] Create requirements.txt for Docker
- [ ] Set up logging configuration
- [ ] Create health check endpoint

**Dependencies**:
```
fastapi
uvicorn
sqlalchemy
alembic
pydantic
python-jose[cryptography]
passlib[bcrypt]
python-multipart
redis
chromadb
langgraph
mcp
```

**Acceptance Criteria**:
- Backend starts with `uvicorn api.main:app --reload`
- Health endpoint returns 200
- Environment variables load correctly

---

### T0.4: Set Up Database Migrations
**Complexity**: S (2-4 hours)
**Files**: backend/database/, alembic.ini

**Tasks**:
- [ ] Configure SQLAlchemy engine
- [ ] Create database models (Users, Products, Reviews, etc.)
- [ ] Set up Alembic for migrations
- [ ] Create initial migration
- [ ] Test migration up/down

**Acceptance Criteria**:
- `alembic upgrade head` creates all tables
- `alembic downgrade -1` removes last migration
- Models match DB.md schema

---

### T0.5: Implement User Model and JWT Auth
**Complexity**: M (1-2 days)
**Files**: backend/database/models.py, backend/services/auth.py, backend/api/routes/auth.py

**Tasks**:
- [ ] Create User model with fields from DB.md
- [ ] Implement password hashing with bcrypt
- [ ] Create JWT token generation/validation
- [ ] Implement register endpoint
- [ ] Implement login endpoint
- [ ] Implement token refresh endpoint
- [ ] Add role-based access control

**Acceptance Criteria**:
- POST /auth/register creates user
- POST /auth/login returns tokens
- POST /auth/refresh generates new access token
- Protected endpoints require valid token

---

### T0.6: Create Base API Middleware
**Complexity**: S (2-4 hours)
**Files**: backend/api/middleware/, backend/api/main.py

**Tasks**:
- [ ] Add CORS middleware
- [ ] Add request logging middleware
- [ ] Add error handling middleware
- [ ] Add rate limiting middleware (Redis-backed)
- [ ] Configure API documentation (Swagger/ReDoc)

**Acceptance Criteria**:
- CORS allows frontend domain
- Errors return consistent JSON format
- Rate limits enforced per endpoint
- API docs accessible at /docs

---

## Phase 1: Core Agent System (Days 3-5)

**Goal**: LangGraph workflow with all 8 agents

### T1.1: Set Up LangGraph StateGraph
**Complexity**: M (1-2 days)
**Files**: backend/graph/state.py, backend/graph/workflow.py

**Tasks**:
- [ ] Define state schema (TypedDict)
- [ ] Create StateGraph instance
- [ ] Add nodes for each agent
- [ ] Define edges and conditional routing
- [ ] Add reflection loop logic
- [ ] Test basic workflow execution

**Acceptance Criteria**:
- Graph executes linear flow
- Reflection agent can trigger retries
- State persists through workflow

---

### T1.2: Implement User Intent Agent
**Complexity**: S (2-4 hours)
**Files**: backend/agents/intent_agent.py

**Tasks**:
- [ ] Parse user query
- [ ] Extract product category
- [ ] Extract budget constraints
- [ ] Extract brand preferences
- [ ] Extract specifications
- [ ] Return structured intent

**Acceptance Criteria**:
- Input: "Find gaming laptop under 1 lakh"
- Output: {category: "laptops", budget: 100000, use_case: "gaming"}

---

### T1.3: Implement Product Search Agent
**Complexity**: L (3-5 days)
**Files**: backend/agents/search_agent.py

**Tasks**:
- [ ] Connect to Product MCP Server
- [ ] Search by category and filters
- [ ] Rank by relevance and rating
- [ ] Handle multiple data sources
- [ ] Cache results in Redis
- [ ] Return top N products

**Acceptance Criteria**:
- Returns 5-10 relevant products
- Products match budget constraints
- Results include key specs

---

### T1.4: Implement Review Analysis Agent
**Complexity**: M (1-2 days)
**Files**: backend/agents/review_agent.py

**Tasks**:
- [ ] Fetch reviews from Review MCP Server
- [ ] Analyze sentiment (LLM-based)
- [ ] Extract pros and cons
- [ ] Calculate aggregate rating
- [ ] Identify review patterns

**Acceptance Criteria**:
- Returns sentiment score (-1 to 1)
- Lists top 3 pros and cons
- Provides review summary

---

### T1.5: Implement Comparison Agent
**Complexity**: S (2-4 hours)
**Files**: backend/agents/comparison_agent.py

**Tasks**:
- [ ] Accept 2-3 product IDs
- [ ] Fetch product details
- [ ] Compare specifications
- [ ] Compare prices
- [ ] Compare ratings
- [ ] Generate comparison table

**Acceptance Criteria**:
- Returns structured comparison
- Highlights best in each category
- Provides overall winner

---

### T1.6: Implement Recommendation Agent
**Complexity**: M (1-2 days)
**Files**: backend/agents/recommendation_agent.py

**Tasks**:
- [ ] Score products on multiple factors
- [ ] Apply user preferences
- [ ] Calculate value-for-money score
- [ ] Rank products
- [ ] Generate reasoning for each
- [ ] Categorize: Best Overall, Budget Pick, Premium

**Acceptance Criteria**:
- Returns 3-5 ranked recommendations
- Each has score and reasoning
- Categories assigned correctly

---

### T1.7: Implement Deal Finder Agent
**Complexity**: S (2-4 hours)
**Files**: backend/agents/deal_agent.py

**Tasks**:
- [ ] Connect to Deals MCP Server
- [ ] Search for coupons
- [ ] Find discount offers
- [ ] Check cashback options
- [ ] Return aggregated deals

**Acceptance Criteria**:
- Returns available deals for products
- Includes discount percentage
- Shows final price after deals

---

### T1.8: Implement Price Tracking Agent
**Complexity**: S (2-4 hours)
**Files**: backend/agents/price_agent.py

**Tasks**:
- [ ] Connect to Pricing MCP Server
- [ ] Fetch price history
- [ ] Analyze price trends
- [ ] Predict price drops
- [ ] Calculate best time to buy

**Acceptance Criteria**:
- Returns price history
- Provides trend analysis
- Predicts next sale period

---

### T1.9: Implement Reflection Agent
**Complexity**: M (1-2 days)
**Files**: backend/agents/reflection_agent.py

**Tasks**:
- [ ] Validate recommendation quality
- [ ] Check for hallucinations
- [ ] Verify product availability
- [ ] Ensure budget compliance
- [ ] Trigger retry if validation fails
- [ ] Log reflection decisions

**Acceptance Criteria**:
- Catches invalid recommendations
- Retries up to 3 times
- Logs all validation decisions

---

### T1.10: Wire Agents into LangGraph Workflow
**Complexity**: M (1-2 days)
**Files**: backend/graph/workflow.py

**Tasks**:
- [ ] Connect all agent nodes
- [ ] Define execution order
- [ ] Add conditional edges for reflection
- [ ] Implement parallel execution where possible
- [ ] Add error handling
- [ ] Test full workflow end-to-end

**Acceptance Criteria**:
- Complete workflow executes
- Reflection triggers on failure
- Final output is validated

---

## Phase 2: MCP Servers (Days 6-7)

**Goal**: Expose shopping tools via Model Context Protocol

### T2.1: Set Up MCP Server Framework
**Complexity**: S (2-4 hours)
**Files**: backend/mcp_servers/__init__.py

**Tasks**:
- [ ] Install FastMCP library
- [ ] Create base MCP server class
- [ ] Add tool registration pattern
- [ ] Set up server startup
- [ ] Create health check tools

**Acceptance Criteria**:
- MCP server starts successfully
- Tools can be registered
- Health check works

---

### T2.2: Implement Product MCP Server
**Complexity**: M (1-2 days)
**Files**: backend/mcp_servers/product_server.py

**Tools**:
- `search_products(query, filters)` - Search products
- `get_product_details(product_id)` - Get full product info
- `compare_products(product_ids)` - Compare products
- `recommend_products(criteria)` - Get recommendations

**Acceptance Criteria**:
- All tools return valid data
- Tools connect to PostgreSQL
- Error handling in place

---

### T2.3: Implement Review MCP Server
**Complexity**: S (2-4 hours)
**Files**: backend/mcp_servers/review_server.py

**Tools**:
- `fetch_reviews(product_id, limit)` - Get reviews
- `summarize_reviews(product_id)` - Get review summary
- `analyze_sentiment(review_text)` - Sentiment analysis

**Acceptance Criteria**:
- Tools return structured review data
- Sentiment analysis works
- Summaries are accurate

---

### T2.4: Implement Pricing MCP Server
**Complexity**: S (2-4 hours)
**Files**: backend/mcp_servers/pricing_server.py

**Tools**:
- `track_price(product_id, target_price)` - Start tracking
- `get_price_history(product_id, period)` - Get history
- `predict_price_drop(product_id)` - Predict next drop

**Acceptance Criteria**:
- Price tracking creates records
- History returns time-series data
- Predictions are reasonable

---

### T2.5: Implement Deals MCP Server
**Complexity**: S (2-4 hours)
**Files**: backend/mcp_servers/deals_server.py

**Tools**:
- `find_discounts(product_id)` - Find discounts
- `find_coupons(product_id)` - Find coupons
- `get_cashback_offers(product_id)` - Get cashback

**Acceptance Criteria**:
- Returns available deals
- Includes discount codes
- Shows cashback percentages

---

### T2.6: Connect Agents to MCP Servers
**Complexity**: M (1-2 days)
**Files**: backend/agents/*.py, backend/graph/workflow.py

**Tasks**:
- [ ] Initialize MCP servers in workflow
- [ ] Pass MCP clients to agents
- [ ] Handle MCP server failures
- [ ] Add retry logic for MCP calls
- [ ] Test agent-MCP integration

**Acceptance Criteria**:
- Agents successfully call MCP tools
- Failures are handled gracefully
- Full workflow uses MCP servers

---

## Phase 3: RAG & Memory (Days 8-9)

**Goal**: Vector search and conversational memory

### T3.1: Set Up ChromaDB Collections
**Complexity**: S (2-4 hours)
**Files**: backend/services/rag.py

**Tasks**:
- [ ] Create products collection
- [ ] Create manuals collection
- [ ] Create FAQs collection
- [ ] Configure embedding model
- [ ] Test vector operations

**Acceptance Criteria**:
- Collections created successfully
- Documents can be added and queried
- Semantic search works

---

### T3.2: Implement Product Data Ingestion
**Complexity**: S (2-4 hours)
**Files**: backend/services/rag.py

**Tasks**:
- [ ] Create ingestion pipeline
- [ ] Parse product specifications
- [ ] Generate embeddings
- [ ] Store in ChromaDB
- [ ] Handle updates and deletes

**Acceptance Criteria**:
- Products are indexed correctly
- Updates propagate to vector store
- Search returns relevant results

---

### T3.3: Build Semantic Search
**Complexity**: S (2-4 hours)
**Files**: backend/services/rag.py

**Tasks**:
- [ ] Implement search function
- [ ] Add filtering by metadata
- [ ] Rank by relevance score
- [ ] Return top K results
- [ ] Add search caching

**Acceptance Criteria**:
- Search returns relevant products
- Results are ranked by relevance
- Response time < 500ms

---

### T3.4: Implement Conversational Memory
**Complexity**: M (1-2 days)
**Files**: backend/services/memory.py

**Tasks**:
- [ ] Create Redis-backed memory store
- [ ] Store conversation history
- [ ] Track user preferences
- [ ] Implement memory retrieval
- [ ] Add memory expiration

**Acceptance Criteria**:
- Memory persists across sessions
- Preferences are recalled
- Memory respects TTL

---

### T3.5: Add User Preference Tracking
**Complexity**: S (2-4 hours)
**Files**: backend/services/memory.py

**Tasks**:
- [ ] Track searched categories
- [ ] Track preferred brands
- [ ] Track budget ranges
- [ ] Track saved products
- [ ] Update preferences on interactions

**Acceptance Criteria**:
- Preferences are captured
- Preferences influence recommendations
- Preferences can be reset

---

### T3.6: Integrate RAG into Agent Workflows
**Complexity**: M (1-2 days)
**Files**: backend/agents/*.py

**Tasks**:
- [ ] Add RAG search to search agent
- [ ] Use memory in recommendation agent
- [ ] Incorporate user preferences
- [ ] Test end-to-end flow
- [ ] Measure improvement

**Acceptance Criteria**:
- RAG enhances search results
- Memory improves personalization
- Recommendations are more relevant

---

## Phase 4: API Layer (Days 10-11)

**Goal**: RESTful API endpoints for frontend

### T4.1: Implement POST /chat
**Complexity**: M (1-2 days)
**Files**: backend/api/routes/chat.py

**Tasks**:
- [ ] Create chat endpoint
- [ ] Handle message input
- [ ] Execute LangGraph workflow
- [ ] Return response with products
- [ ] Store in chat history
- [ ] Add WebSocket support

**Acceptance Criteria**:
- Endpoint accepts messages
- Returns AI response
- History is saved

---

### T4.2: Implement POST /recommend
**Complexity**: S (2-4 hours)
**Files**: backend/api/routes/products.py

**Tasks**:
- [ ] Create recommendation endpoint
- [ ] Accept category and preferences
- [ ] Execute recommendation agent
- [ ] Return ranked products
- [ ] Include reasoning

**Acceptance Criteria**:
- Returns personalized recommendations
- Products match criteria
- Reasoning is provided

---

### T4.3: Implement POST /compare
**Complexity**: S (2-4 hours)
**Files**: backend/api/routes/products.py

**Tasks**:
- [ ] Create comparison endpoint
- [ ] Accept product IDs
- [ ] Execute comparison agent
- [ ] Return comparison table
- [ ] Highlight winner

**Acceptance Criteria**:
- Returns structured comparison
- All products included
- Winner is identified

---

### T4.4: Implement POST /track-price
**Complexity**: S (2-4 hours)
**Files**: backend/api/routes/products.py

**Tasks**:
- [ ] Create price tracking endpoint
- [ ] Accept product ID and target price
- [ ] Create tracking record
- [ ] Return confirmation
- [ ] Schedule price checks

**Acceptance Criteria**:
- Tracking record created
- Confirmation returned
- Price checks scheduled

---

### T4.5: Implement GET /price-history
**Complexity**: S (2-4 hours)
**Files**: backend/api/routes/products.py

**Tasks**:
- [ ] Create price history endpoint
- [ ] Accept product ID and period
- [ ] Fetch from Pricing MCP Server
- [ ] Return time-series data
- [ ] Include statistics

**Acceptance Criteria**:
- Returns price history
- Includes min/max/avg
- Trend analysis included

---

### T4.6: Implement POST /autonomous-research
**Complexity**: M (1-2 days)
**Files**: backend/api/routes/research.py

**Tasks**:
- [ ] Create research endpoint
- [ ] Accept research query
- [ ] Execute full workflow
- [ ] Generate comprehensive report
- [ ] Return structured output

**Acceptance Criteria**:
- Completes full research
- Returns comprehensive report
- Includes all analysis types

---

### T4.7: Implement GET /analytics
**Complexity**: S (2-4 hours)
**Files**: backend/api/routes/analytics.py

**Tasks**:
- [ ] Create analytics endpoint
- [ ] Aggregate user data
- [ ] Calculate platform metrics
- [ ] Return analytics object

**Acceptance Criteria**:
- Returns user analytics
- Returns platform analytics
- Data is accurate

---

### T4.8: Add API Documentation
**Complexity**: XS (<1 hour)
**Files**: backend/api/main.py

**Tasks**:
- [ ] Configure OpenAPI schema
- [ ] Add endpoint descriptions
- [ ] Add request/response examples
- [ ] Test Swagger UI
- [ ] Test ReDoc

**Acceptance Criteria**:
- Swagger UI accessible at /docs
- All endpoints documented
- Examples are accurate

---

## Phase 5: Frontend (Days 12-15)

**Goal**: Next.js UI with all pages

### T5.1: Set Up Next.js Project
**Complexity**: M (1-2 days)
**Files**: frontend/

**Tasks**:
- [ ] Initialize Next.js with TypeScript
- [ ] Configure TailwindCSS
- [ ] Set up Shadcn UI
- [ ] Create API client
- [ ] Set up authentication context
- [ ] Create layout components

**Acceptance Criteria**:
- Project builds successfully
- Tailwind works
- Components render

---

### T5.2: Implement Auth Pages
**Complexity**: S (2-4 hours)
**Files**: frontend/app/login/, frontend/app/register/

**Tasks**:
- [ ] Create login form
- [ ] Create register form
- [ ] Add form validation
- [ ] Implement auth flow
- [ ] Add error handling
- [ ] Create protected route wrapper

**Acceptance Criteria**:
- Login works
- Register works
- Redirects on success

---

### T5.3: Build Chat Interface
**Complexity**: L (3-5 days)
**Files**: frontend/app/chat/, frontend/components/chat/

**Tasks**:
- [ ] Create message components
- [ ] Create input component
- [ ] Add typing indicator
- [ ] Implement message history
- [ ] Add product cards in messages
- [ ] Add WebSocket support
- [ ] Handle loading states

**Acceptance Criteria**:
- Messages display correctly
- Input works
- Products show in messages
- Real-time updates

---

### T5.4: Build Product Dashboard
**Complexity**: M (1-2 days)
**Files**: frontend/app/products/, frontend/components/products/

**Tasks**:
- [ ] Create product grid
- [ ] Add filters sidebar
- [ ] Implement search
- [ ] Create product cards
- [ ] Add pagination
- [ ] Create product detail page

**Acceptance Criteria**:
- Products display in grid
- Filters work
- Search works
- Detail page shows full info

---

### T5.5: Build Analytics Dashboard
**Complexity**: M (1-2 days)
**Files**: frontend/app/analytics/, frontend/components/charts/

**Tasks**:
- [ ] Create chart components
- [ ] Add search trends chart
- [ ] Add category distribution
- [ ] Add recommendation accuracy
- [ ] Create stats cards

**Acceptance Criteria**:
- Charts render correctly
- Data is accurate
- Responsive layout

---

### T5.6: Build Saved Products Page
**Complexity**: S (2-4 hours)
**Files**: frontend/app/saved/

**Tasks**:
- [ ] Create saved products list
- [ ] Add remove functionality
- [ ] Add price tracking toggle
- [ ] Create empty state

**Acceptance Criteria**:
- Saved products display
- Remove works
- Tracking toggle works

---

### T5.7: Build Price Tracker Page
**Complexity**: M (1-2 days)
**Files**: frontend/app/tracker/, frontend/components/tracker/

**Tasks**:
- [ ] Create tracked products list
- [ ] Add price history chart
- [ ] Show current vs target price
- [ ] Add alerts section
- [ ] Create tracking management

**Acceptance Criteria**:
- Tracked products display
- Price charts work
- Alerts show correctly

---

### T5.8: Integrate Frontend with Backend
**Complexity**: M (1-2 days)
**Files**: frontend/lib/api.ts

**Tasks**:
- [ ] Create API client functions
- [ ] Add auth headers
- [ ] Handle errors
- [ ] Add loading states
- [ ] Test all integrations

**Acceptance Criteria**:
- All API calls work
- Auth is handled
- Errors display correctly

---

## Phase 6: Production Hardening (Days 16-17)

**Goal**: Testing, security, deployment

### T6.1: Write Unit Tests
**Complexity**: L (3-5 days)
**Files**: backend/tests/unit/

**Tasks**:
- [ ] Test intent agent
- [ ] Test search agent
- [ ] Test review agent
- [ ] Test comparison agent
- [ ] Test recommendation agent
- [ ] Test deal agent
- [ ] Test price agent
- [ ] Test reflection agent

**Acceptance Criteria**:
- 80%+ coverage for agents
- All tests pass
- Edge cases covered

---

### T6.2: Write Integration Tests
**Complexity**: M (1-2 days)
**Files**: backend/tests/integration/

**Tasks**:
- [ ] Test MCP servers
- [ ] Test database operations
- [ ] Test Redis operations
- [ ] Test ChromaDB operations

**Acceptance Criteria**:
- MCP servers work correctly
- Database operations succeed
- Cache operations work

---

### T6.3: Write API Tests
**Complexity**: M (1-2 days)
**Files**: backend/tests/api/

**Tasks**:
- [ ] Test auth endpoints
- [ ] Test chat endpoints
- [ ] Test product endpoints
- [ ] Test analytics endpoints

**Acceptance Criteria**:
- All endpoints tested
- Auth flows work
- Error handling works

---

### T6.4: Add Input Validation
**Complexity**: S (2-4 hours)
**Files**: backend/api/schemas.py

**Tasks**:
- [ ] Validate all request bodies
- [ ] Sanitize user input
- [ ] Add rate limiting
- [ ] Prevent SQL injection
- [ ] Add CSRF protection

**Acceptance Criteria**:
- Invalid inputs rejected
- Malicious input blocked
- Rate limits enforced

---

### T6.5: Add Rate Limiting
**Complexity**: S (2-4 hours)
**Files**: backend/api/middleware/rate_limit.py

**Tasks**:
- [ ] Implement Redis-based rate limiting
- [ ] Configure per-endpoint limits
- [ ] Add rate limit headers
- [ ] Handle rate limit exceeded

**Acceptance Criteria**:
- Limits enforced
- Headers present
- Proper error on exceed

---

### T6.6: Add Logging and Monitoring
**Complexity**: S (2-4 hours)
**Files**: backend/logging_config.py

**Tasks**:
- [ ] Configure structured logging
- [ ] Add request logging
- [ ] Add error logging
- [ ] Add performance metrics
- [ ] Create health check endpoint

**Acceptance Criteria**:
- Logs are structured
- Errors are captured
- Metrics available

---

### T6.7: Create Deployment Configs
**Complexity**: M (1-2 days)
**Files**: docker/, deploy/

**Tasks**:
- [ ] Create production Dockerfile
- [ ] Create deployment scripts
- [ ] Configure environment variables
- [ ] Set up CI/CD pipeline
- [ ] Create deployment documentation

**Acceptance Criteria**:
- Docker image builds
- Deployment works
- Docs are complete

---

### T6.8: Write Deployment Documentation
**Complexity**: S (2-4 hours)
**Files**: docs/DEPLOYMENT.md

**Tasks**:
- [ ] Document deployment steps
- [ ] Document environment setup
- [ ] Document scaling procedures
- [ ] Document troubleshooting

**Acceptance Criteria**:
- Steps are clear
- All configs documented
- Troubleshooting included

---

## Verification Strategy

### Backend Testing
```bash
# Unit tests
pytest backend/tests/unit/ -v

# Integration tests
pytest backend/tests/integration/ -v

# API tests
pytest backend/tests/api/ -v

# Coverage
pytest --cov=backend backend/tests/
```

### Frontend Testing
```bash
# Unit tests
npm test --prefix frontend

# E2E tests
npm run test:e2e --prefix frontend
```

### Infrastructure Testing
```bash
# Docker build
docker-compose build

# Service health
docker-compose ps

# Load testing
locust -f tests/load/locustfile.py
```

---

## Documentation Checklist

After each phase, update:

- [ ] ARCH.md - Architecture diagrams
- [ ] API.md - New endpoints
- [ ] DB.md - Schema changes
- [ ] FLOW.md - New user journeys
- [ ] README.md - Setup instructions

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM API costs exceed budget | High | Implement caching, use smaller models |
| MCP server instability | Medium | Add retry logic, fallback responses |
| Database performance | Medium | Connection pooling, query optimization |
| Frontend bundle size | Low | Code splitting, lazy loading |
| Security vulnerabilities | High | Regular audits, dependency updates |
