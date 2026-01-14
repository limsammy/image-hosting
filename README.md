# Image Hosting App

A minimalist image hosting service with drag-and-drop uploads, user authentication, and Cloudflare R2 storage.

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.0+-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.109+-green.svg)
![React](https://img.shields.io/badge/react-18+-61dafb.svg)

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.12+ with [uv](https://github.com/astral-sh/uv) (for local backend development)

### Run with Docker

```bash
# Clone and enter the project
cd image_hosting

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker-compose up --build
```

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Local Development

```bash
# Backend (from backend/)
uv sync
uv run uvicorn app.main:app --reload

# Frontend (from frontend/)
npm install
npm run dev
```

## Documentation

| Document | Description |
|----------|-------------|
| [Setup Guide](docs/setup.md) | Detailed installation and configuration |
| [Development](docs/development.md) | Development workflow and commands |
| [Architecture](docs/architecture.md) | System design and decisions |
| [Environment Variables](docs/environment.md) | All configuration options |
| [Implementation Plan](PLAN.md) | Phased development roadmap |

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, SQLAlchemy 2.0, PostgreSQL, Pydantic |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS |
| **Storage** | Cloudflare R2 (S3-compatible) |
| **Auth** | JWT with bcrypt password hashing |
| **DevOps** | Docker Compose, uv, npm |

## Project Structure

```
image_hosting/
├── backend/           # FastAPI Python backend
│   ├── app/
│   │   ├── models/    # SQLAlchemy ORM models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── routers/   # API endpoints
│   │   └── services/  # Business logic
│   └── tests/
├── frontend/          # React TypeScript frontend
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── hooks/
│       └── context/
├── docs/              # Documentation
└── docker-compose.yml
```

## License

MIT
