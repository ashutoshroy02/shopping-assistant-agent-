# AGENTS.md - AI Coding Agent Configuration

## Project Context

**AI Shopping Assistant Platform** - Multi-agent system for autonomous product research, comparison, and recommendations.

**Tech Stack**: Python, LangGraph, MCP, FastAPI, PostgreSQL, Redis, ChromaDB, Next.js, TypeScript

## Current Phase

**Phase 0: Foundation** - Project scaffolding, database setup, authentication

## File Structure

```
shopping-assistant/
├── backend/
│   ├── agents/          # LangGraph agent implementations
│   ├── graph/           # StateGraph workflow
│   ├── mcp_servers/     # MCP tool servers
│   ├── api/             # FastAPI routes
│   ├── database/        # Models, schemas, migrations
│   ├── services/        # Business logic
│   └── tests/           # Unit and integration tests
├── frontend/
│   ├── app/             # Next.js pages
│   ├── components/      # React components
│   ├── hooks/           # Custom hooks
│   └── lib/             # Utilities, API client
├── docs/                # Documentation
└── docker/              # Docker configs
```

## Conventions

### Python Backend
- Use async/await for all I/O operations
- Pydantic models for request/response validation
- Type hints on all functions
- Docstrings for public APIs
- Error handling with custom exceptions

### TypeScript Frontend
- Strict TypeScript configuration
- Server components by default, client components when needed
- TailwindCSS for styling
- Shadcn UI components

### Git Workflow
- Feature branches from `main`
- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
- PR reviews required before merge

## Rules

1. **Never commit secrets** - Use environment variables
2. **Test before commit** - Run `pytest` and `npm test`
3. **Update docs** - Keep ARCH.md, API.md in sync
4. **Follow patterns** - Match existing code style
5. **Small PRs** - One feature per pull request

## Testing

```bash
# Backend tests
pytest backend/tests/ -v

# Frontend tests
npm test --prefix frontend

# Coverage
pytest --cov=backend backend/tests/
```

## Common Commands

```bash
# Start development
docker-compose up -d
cd backend && uvicorn api.main:app --reload
cd frontend && npm run dev

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "description"

# Run tests
pytest
npm test
```

## Current Tasks

See `docs/IMPL-PLAN.md` for detailed task breakdown.

## References

- `docs/ARCH.md` - System architecture
- `docs/API.md` - API specifications
- `docs/DB.md` - Database schema
- `docs/FLOW.md` - User journeys
- `plan.md` - Original project plan
