# Contributing to AI Shopping Assistant

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/shopping-assistant.git
   cd shopping-assistant
   ```

3. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

5. Set up environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. Start services:
   ```bash
   docker-compose up -d
   ```

## 📝 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow the code style guidelines below
- Write tests for new features
- Update documentation if needed

### 3. Run Tests

```bash
# Backend
cd backend
pytest -v

# Frontend
cd frontend
npm test
```

### 4. Lint Your Code

```bash
# Backend
cd backend
ruff check .
ruff format .

# Frontend
cd frontend
npm run lint
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 🎨 Code Style

### Python (Backend)

- Use **type hints** on all functions
- Follow **PEP 8** style guide
- Use **async/await** for I/O operations
- Keep functions **short and focused**
- Add **docstrings** to public APIs

```python
async def get_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Product:
    """Fetch a product by ID.
    
    Args:
        product_id: The product UUID
        db: Database session
        
    Returns:
        Product object
        
    Raises:
        NotFoundException: If product not found
    """
    pass
```

### TypeScript (Frontend)

- Use **strict TypeScript**
- Prefer **server components** when possible
- Use **functional components** with hooks
- Follow **Shadcn UI** patterns

```typescript
interface ProductCardProps {
  product: Product
  compact?: boolean
}

export function ProductCard({ product, compact }: ProductCardProps) {
  return (
    <div className="border rounded-lg p-4">
      {/* Content */}
    </div>
  )
}
```

## 🧪 Testing Guidelines

### Unit Tests

- Test individual functions/methods
- Mock external dependencies
- Aim for **80%+ coverage**

```python
def test_extract_budget():
    result = extract_budget("Find laptop under 100000")
    assert result == {"min": 0, "max": 100000}
```

### Integration Tests

- Test API endpoints
- Test database operations
- Test agent workflows

```python
@pytest.mark.asyncio
async def test_chat_endpoint(client, auth_headers):
    response = await client.post(
        "/api/v1/chat",
        json={"message": "Find laptops"},
        headers=auth_headers,
    )
    assert response.status_code == 200
```

### Test File Naming

- Unit tests: `test_<module>.py`
- API tests: `test_<endpoint>.py`
- Integration tests: `test_<feature>.py`

## 📋 Pull Request Guidelines

### PR Title

Use conventional commits:

```
feat: add price tracking feature
fix: resolve chat session bug
docs: update API documentation
test: add unit tests for agents
```

### PR Description

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🐛 Reporting Issues

### Bug Reports

Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment details

### Feature Requests

Include:
- Problem description
- Proposed solution
- Alternatives considered
- Additional context

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## ❓ Questions?

Feel free to open an issue with the `question` label or start a discussion in the repository.

Thank you for contributing! 🎉
