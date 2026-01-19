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

R2 provides S3-compatible object storage with a generous free tier (10GB storage, no egress fees).

### 1. Create R2 Bucket

1. Log into [Cloudflare Dashboard](https://dash.cloudflare.com) → R2 Object Storage
2. Click "Create bucket" → Name it `image-hosting`
3. Note your **Account ID** from the dashboard URL: `dash.cloudflare.com/<ACCOUNT_ID>/r2`

### 2. Generate API Credentials

1. In R2 dashboard → "Manage R2 API Tokens" → "Create API Token"
2. Permissions: **Object Read & Write**
3. Scope: Specific bucket → `image-hosting`
4. Save both the **Access Key ID** and **Secret Access Key** (shown only once)

### 3. Enable Public Access

1. Select your bucket → Settings → Public access
2. Click "Allow Access" → Choose **R2.dev subdomain**
3. Copy the public URL (e.g., `https://pub-xxx.r2.dev`)

### 4. Update Environment Variables

Update `backend/.env` with:
```bash
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY=your_access_key_id
R2_SECRET_KEY=your_secret_access_key
R2_BUCKET_NAME=image-hosting
R2_PUBLIC_URL=https://pub-xxx.r2.dev
```

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
