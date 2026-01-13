# Task Completion Checklist

When completing a task, ensure the following steps are performed:

## After Code Changes

### Backend Changes
1. **Run tests**: `cd backend && uv run pytest`
2. **Run tests with coverage**: `cd backend && uv run pytest --cov=app --cov-report=html`
3. **Check for type issues**: Ensure all type hints are correct

### Frontend Changes
1. **Run tests**: `cd frontend && npm run test`
2. **Run tests with coverage**: `cd frontend && npm run test:coverage`
3. **Type check**: TypeScript compiler should pass

### Database Changes
1. **Create migration**: `cd backend && uv run alembic revision --autogenerate -m "description"`
2. **Run migration**: `cd backend && uv run alembic upgrade head`
3. **Verify migration**: Check that database schema matches models

## Full Stack Verification
1. Start all services: `docker-compose up --build`
2. Health check: `curl http://localhost:8000/api/health`
3. Manual test affected functionality

## Before Committing
1. Ensure all tests pass
2. Review changed files
3. Write clear commit message describing the changes
