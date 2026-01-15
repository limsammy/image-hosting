# Image Hosting Backend

FastAPI backend for the image hosting service.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker and Docker Compose

## Setup

### 1. Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

The `.env` file contains:
- `POSTGRES_*` - Database connection (used by both app and Docker)
- `JWT_SECRET_KEY` - Change this in production
- `R2_*` - Cloudflare R2 storage credentials (configure when needed)

### 2. Start Database

```bash
# From project root
docker-compose up db -d
```

PostgreSQL will automatically create the `imagehosting` database using the `POSTGRES_DB` environment variable.

### 3. Run Migrations

```bash
# Using Docker (recommended)
docker-compose --profile tools run --rm migrate

# Or locally (requires POSTGRES_HOST=localhost in .env)
uv run alembic upgrade head
```

### 4. Start Development Server

```bash
# Local development
uv run uvicorn app.main:app --reload

# Or with Docker
docker-compose up backend
```

API will be available at http://localhost:8000

## Database Migrations

```bash
# Generate new migration after model changes
docker-compose run --rm migrate uv run alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose --profile tools run --rm migrate

# View migration history
uv run alembic history
```

## Project Structure

```
backend/
├── app/
│   ├── config.py      # Settings from environment variables
│   ├── database.py    # Async SQLAlchemy setup
│   ├── main.py        # FastAPI application
│   ├── models/        # SQLAlchemy ORM models
│   │   ├── user.py
│   │   └── image.py
│   ├── schemas/       # Pydantic request/response schemas
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── image.py
│   ├── routers/       # API route handlers
│   └── services/      # Business logic
├── alembic/           # Database migrations
├── tests/
└── pyproject.toml
```

## Docker Services

| Service | Description | Port |
|---------|-------------|------|
| `db` | PostgreSQL 16 | Internal only |
| `backend` | FastAPI app | 8000 |
| `migrate` | Run migrations (profile: tools) | - |
