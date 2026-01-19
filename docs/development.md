# Development Workflow

Day-to-day development commands and best practices.

## Quick Reference

### Start Development Environment

**Option A: Docker (all services)**

```bash
# All services
docker-compose up

# Or with rebuild
docker-compose up --build

# Background mode
docker-compose up -d
```

**Option B: Local Development (recommended for backend work)**

```bash
# 1. Set up local PostgreSQL (one-time)
./scripts/setup-local-db.sh

# 2. Update backend/.env with local database settings (see script output)

# 3. Run migrations
cd backend && uv run alembic upgrade head

# 4. Start backend with hot reload
uv run uvicorn app.main:app --reload

# 5. In another terminal, start frontend
cd frontend && npm run dev
```

### Stop Services

```bash
# Docker
docker-compose down

# Also remove volumes (clean slate)
docker-compose down -v
```

## Backend Development

### Running the Server

```bash
cd backend

# With hot reload
uv run uvicorn app.main:app --reload

# Specify port
uv run uvicorn app.main:app --reload --port 8001
```

### Managing Dependencies

```bash
# Add a new dependency
uv add <package>

# Add dev dependency
uv add --dev <package>

# Sync dependencies
uv sync

# Update all dependencies
uv lock --upgrade
```

### Database Operations

```bash
# Run migrations
uv run alembic upgrade head

# Create new migration
uv run alembic revision --autogenerate -m "description"

# Rollback one migration
uv run alembic downgrade -1

# View migration history
uv run alembic history
```

### Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=app --cov-report=html

# Specific test file
uv run pytest tests/unit/test_auth.py

# Verbose output
uv run pytest -v

# Stop on first failure
uv run pytest -x
```

## Frontend Development

### Running the Dev Server

```bash
cd frontend

# Start dev server
npm run dev

# With specific host (for Docker)
npm run dev -- --host
```

### Managing Dependencies

```bash
# Add dependency
npm install <package>

# Add dev dependency
npm install -D <package>

# Update all
npm update
```

### Running Tests

```bash
# Run tests
npm run test

# Watch mode
npm run test:watch

# With coverage
npm run test:coverage
```

### Building for Production

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

## Code Style

### Backend (Python)

- **Async/await**: Use for all I/O operations
- **Type hints**: Required for all function signatures
- **Pydantic**: Use for all request/response validation
- **SQLAlchemy 2.0**: Use `Mapped` type hints for models
- **Loguru**: Use instead of stdlib logging

```python
# Good
async def get_user(user_id: int) -> User:
    ...

# Bad
def get_user(user_id):
    ...
```

### Frontend (TypeScript)

- **Functional components**: No class components
- **Hooks**: Use for state and side effects
- **TypeScript**: Strict mode enabled
- **Tailwind**: No separate CSS files

```tsx
// Good
const UserCard: React.FC<{ user: User }> = ({ user }) => {
  return <div className="p-4 bg-white rounded">{user.name}</div>;
};

// Bad
class UserCard extends React.Component { ... }
```

## Git Workflow

### Commit Messages

Follow conventional commits:

```
feat: add user registration endpoint
fix: resolve JWT token expiration issue
docs: update API documentation
refactor: extract auth service
test: add integration tests for images API
```

### Branch Naming

```
feature/user-authentication
fix/upload-validation
docs/api-reference
```

## Docker Tips

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Execute Commands in Container

```bash
# Backend shell
docker-compose exec backend bash

# Run migrations in container
docker-compose exec backend uv run alembic upgrade head

# Frontend shell
docker-compose exec frontend sh
```

### Rebuild Single Service

```bash
docker-compose up --build backend
```

## Debugging

### Backend

Use `loguru` for debugging:

```python
from loguru import logger

logger.debug(f"Processing user: {user_id}")
logger.error(f"Failed to upload: {error}")
```

### Frontend

Use React DevTools and browser console:

```tsx
console.log('State:', state);
debugger; // Breakpoint
```

### Database

Connect to PostgreSQL:

```bash
# Local development (after running setup script)
psql -U imagehosting_user -d imagehosting_dev -h localhost

# Via Docker container
docker-compose exec db psql -U postgres -d imagehosting
```

## API Documentation

FastAPI auto-generates interactive docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
