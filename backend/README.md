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
- `R2_*` - Cloudflare R2 storage credentials (see below)

### 2. Configure Cloudflare R2 Storage

R2 provides S3-compatible object storage with a generous free tier (10GB storage, no egress fees).

#### Create R2 Bucket
1. Log into [Cloudflare Dashboard](https://dash.cloudflare.com) → R2 Object Storage
2. Click "Create bucket" → Name it `image-hosting`
3. Note your **Account ID** from the dashboard URL: `dash.cloudflare.com/<ACCOUNT_ID>/r2`

#### Generate API Credentials
1. In R2 dashboard → "Manage R2 API Tokens" → "Create API Token"
2. Permissions: **Object Read & Write**
3. Scope: Specific bucket → `image-hosting`
4. Save both the **Access Key ID** and **Secret Access Key** (shown only once)

#### Enable Public Access
1. Select your bucket → Settings → Public access
2. Click "Allow Access" → Choose **R2.dev subdomain**
3. Copy the public URL (e.g., `https://pub-xxx.r2.dev`)

#### Update `.env`
```bash
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY=your_access_key_id
R2_SECRET_KEY=your_secret_access_key
R2_BUCKET_NAME=image-hosting
R2_PUBLIC_URL=https://pub-xxx.r2.dev
```

### 3. Start Database

```bash
# From project root
docker-compose up db -d
```

PostgreSQL will automatically create the `imagehosting` database using the `POSTGRES_DB` environment variable.

### 4. Run Migrations

```bash
# Using Docker (recommended)
docker-compose --profile tools run --rm migrate

# Or locally (requires POSTGRES_HOST=localhost in .env)
uv run alembic upgrade head
```

### 5. Start Development Server

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
│   │   ├── auth.py    # Auth endpoints (register, login, /me)
│   │   └── images.py  # Image endpoints (upload, list, delete)
│   └── services/      # Business logic
│       ├── auth.py    # Password hashing, JWT tokens
│       └── storage.py # R2 storage (presigned URLs, verification)
├── alembic/           # Database migrations
├── tests/
└── pyproject.toml
```

## Testing

Tests use pytest with pytest-asyncio for async support and an in-memory SQLite database.

```bash
# Install dev dependencies
uv sync --all-extras

# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run only unit tests
uv run pytest tests/unit/

# Run only integration tests
uv run pytest tests/integration/
```

### Test Structure

```
tests/
├── conftest.py                 # Shared fixtures (async client, test DB)
├── unit/
│   ├── test_auth_service.py    # Unit tests for AuthService
│   └── test_storage_service.py # Unit tests for R2Storage (moto mocks)
└── integration/
    ├── test_auth_api.py        # Auth API endpoint tests
    └── test_images_api.py      # Images API endpoint tests
```

## Docker Services

| Service | Description | Port |
|---------|-------------|------|
| `db` | PostgreSQL 16 | Internal only |
| `backend` | FastAPI app | 8000 |
| `migrate` | Run migrations (profile: tools) | - |
