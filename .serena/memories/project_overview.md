# Image Hosting App - Project Overview

## Purpose
A minimalist image hosting service with drag-and-drop uploads, user authentication, and Cloudflare R2 storage.

## Tech Stack
| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, SQLAlchemy, PostgreSQL, Pydantic |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS |
| **Image Storage** | Cloudflare R2 (S3-compatible) |
| **Auth** | Username/password with JWT tokens |
| **Package Management** | uv (Python), npm (Node) |
| **Containerization** | Docker Compose |
| **Testing** | pytest + pytest-cov (backend), Vitest + React Testing Library (frontend) |
| **Logging** | Loguru (backend) |

## Architecture
- **Cloudflare R2**: Stores actual image files (bytes). Object storage like AWS S3.
- **PostgreSQL**: Stores structured data (users, image metadata, relationships).

### Upload Flow
1. Frontend requests presigned URL from backend
2. Frontend uploads directly to R2 using presigned URL
3. Frontend confirms upload with backend
4. Backend saves metadata to PostgreSQL

### Auth Flow
1. User registers with username/email/password
2. Password hashed with bcrypt, stored in PostgreSQL
3. Login returns JWT token (7-day expiry)
4. Frontend stores token in localStorage
5. All authenticated requests include `Authorization: Bearer <token>`

## Project Structure
```
image_hosting/
├── backend/           # FastAPI Python backend
│   ├── app/
│   │   ├── models/    # SQLAlchemy ORM models
│   │   ├── schemas/   # Pydantic request/response schemas
│   │   ├── routers/   # API route handlers
│   │   └── services/  # Business logic (auth, storage)
│   └── tests/         # pytest unit + integration tests
├── frontend/          # React TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── context/
│   └── tests/         # Vitest component tests
├── docs/mockups/      # UI/UX wireframes
└── docker-compose.yml
```

## Implementation Status
See PLAN.md for detailed implementation plan (10 phases, 36 steps).
Current Phase: Not started
