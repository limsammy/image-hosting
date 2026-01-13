# Suggested Commands

## Development

### Start All Services
```bash
docker-compose up --build
```

### Backend Only (from backend/)
```bash
uv run uvicorn app.main:app --reload
```

### Frontend Only (from frontend/)
```bash
npm run dev
```

## Testing

### Backend Tests with Coverage
```bash
cd backend && uv run pytest --cov=app --cov-report=html
```

### Backend Unit Tests Only
```bash
cd backend && uv run pytest tests/unit/
```

### Backend Integration Tests Only
```bash
cd backend && uv run pytest tests/integration/
```

### Frontend Tests
```bash
cd frontend && npm run test
```

### Frontend Tests with Coverage
```bash
cd frontend && npm run test:coverage
```

### Frontend Tests Watch Mode
```bash
cd frontend && npm run test:watch
```

## Database

### Run Migrations
```bash
cd backend && uv run alembic upgrade head
```

### Create New Migration
```bash
cd backend && uv run alembic revision --autogenerate -m "description"
```

## Verification

### Health Check
```bash
curl http://localhost:8000/api/health
```

## System Utils (Darwin/macOS)
- `git` - Version control
- `ls` - List files
- `cd` - Change directory
- `grep` - Search text (use `grep -r` for recursive)
- `find` - Find files
- `open` - Open files/URLs in default app
