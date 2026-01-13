# Image Hosting App

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

## Quick Commands

### Development
```bash
# Start all services (PostgreSQL, backend, frontend)
docker-compose up --build

# Backend only (from backend/)
uv run uvicorn app.main:app --reload

# Frontend only (from frontend/)
npm run dev
```

### Testing
```bash
# Backend tests with coverage
cd backend && uv run pytest --cov=app --cov-report=html

# Frontend tests
cd frontend && npm run test

# Frontend tests with coverage
cd frontend && npm run test:coverage
```

### Database
```bash
# Run migrations
cd backend && uv run alembic upgrade head

# Create new migration
cd backend && uv run alembic revision --autogenerate -m "description"
```

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Create new user | No |
| POST | `/api/auth/login` | Get JWT token | No |
| GET | `/api/auth/me` | Get current user | Yes |
| POST | `/api/images/upload-url` | Get presigned R2 URL | Yes |
| POST | `/api/images/confirm` | Confirm upload, save metadata | Yes |
| GET | `/api/images/` | List user's images | Yes |
| DELETE | `/api/images/{id}` | Delete image | Yes |
| GET | `/api/health` | Health check | No |

## Environment Variables

### Backend (`backend/.env`)
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - Secret for JWT signing (min 32 chars)
- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` - Cloudflare R2 credentials
- `R2_BUCKET_NAME`, `R2_PUBLIC_URL` - R2 bucket config
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `FRONTEND_URL` - Frontend URL for CORS

### Frontend (`frontend/.env`)
- `VITE_API_URL` - Backend API URL

## Architecture Notes

### Why R2 + PostgreSQL?
- **Cloudflare R2**: Stores actual image files (bytes). Object storage like AWS S3. 10GB free, unlimited bandwidth.
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

## Implementation Status

See `PLAN.md` for detailed implementation plan (10 phases, 36 steps).

**Current Phase**: Not started

## Code Conventions

### Backend (Python)
- Use async/await for all database and HTTP operations
- Pydantic models for all request/response validation
- SQLAlchemy 2.0 style with `Mapped` type hints
- Loguru for all logging (not stdlib logging)

### Frontend (TypeScript)
- Functional components with hooks
- Context API for global state (auth)
- Axios for API calls with interceptors
- Tailwind for styling (no CSS files)

## Useful Links

- [PLAN.md](./PLAN.md) - Full implementation plan
- [FastAPI docs](https://fastapi.tiangolo.com/)
- [Cloudflare R2 docs](https://developers.cloudflare.com/r2/)
- [React docs](https://react.dev/)
- [Tailwind docs](https://tailwindcss.com/docs)
