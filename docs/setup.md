# Setup Guide

Complete instructions for setting up the Image Hosting App development environment.

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Docker | 24+ | Container runtime |
| Docker Compose | 2.0+ | Multi-container orchestration |
| Node.js | 20+ | Frontend development |
| Python | 3.12+ | Backend development |
| uv | Latest | Python package manager |
| Git | 2.0+ | Version control |

### Installing uv (Python Package Manager)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv
```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd image_hosting
```

### 2. Configure Environment Variables

```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env
```

Edit `backend/.env` with your configuration. See [Environment Variables](environment.md) for details.

### 3. Choose Your Setup Method

#### Option A: Docker (Recommended)

Start all services with a single command:

```bash
docker-compose up --build
```

This starts:
- PostgreSQL database on port 5432
- Backend API on port 8000
- Frontend dev server on port 5173

#### Option B: Local Development

**Backend:**

```bash
cd backend

# Create virtual environment and install dependencies
uv sync

# Install dev dependencies too
uv sync --all-extras

# Run the development server
uv run uvicorn app.main:app --reload
```

**Frontend:**

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

**Database:**

You'll need PostgreSQL running locally or via Docker:

```bash
# Start just the database
docker-compose up db
```

## Verification

### Check Backend

```bash
curl http://localhost:8000/api/health
# Expected: {"status":"healthy"}
```

### Check Frontend

Open http://localhost:5173 in your browser.

### Check API Documentation

Open http://localhost:8000/docs for interactive Swagger UI.

## Cloudflare R2 Setup

To enable image uploads, you need a Cloudflare R2 bucket:

1. Create a Cloudflare account at https://cloudflare.com
2. Navigate to R2 in the dashboard
3. Create a new bucket (e.g., `image-hosting`)
4. Create an API token with R2 read/write permissions
5. Update `backend/.env` with:
   - `R2_ACCOUNT_ID`
   - `R2_ACCESS_KEY_ID`
   - `R2_SECRET_ACCESS_KEY`
   - `R2_BUCKET_NAME`
   - `R2_PUBLIC_URL` (your bucket's public URL)

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>
```

### Database Connection Failed

Ensure PostgreSQL is running:

```bash
docker-compose ps db
```

### Python Dependencies Not Found

Ensure you're in the virtual environment:

```bash
cd backend
uv sync
uv run python -c "import fastapi; print('OK')"
```

## Next Steps

- Read [Development Workflow](development.md) for day-to-day commands
- Review [Architecture](architecture.md) to understand the system design
- Check [Environment Variables](environment.md) for all configuration options
