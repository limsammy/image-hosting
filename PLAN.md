# Image Hosting App - Implementation Plan

## Overview
A minimalist image hosting service with:
- **Backend**: FastAPI (Python) with SQLAlchemy ORM
- **Frontend**: React + Vite + TypeScript + Tailwind CSS
- **Image Storage**: Cloudflare R2 (S3-compatible, 10GB free, unlimited bandwidth)
- **Database**: PostgreSQL (user accounts, image metadata)
- **Auth**: Username/password with JWT tokens
- **Package Management**: uv (modern Python package manager)
- **Containerization**: Docker Compose

## Features
- User registration and login (username/password)
- Drag-and-drop image upload (direct to R2 via presigned URLs)
- Gallery view with CSS-based thumbnails
- One-click copy URL to clipboard
- Delete images
- Comprehensive logging (Loguru)

## Architecture

### Why R2 + PostgreSQL?
| Component | Purpose |
|-----------|---------|
| **Cloudflare R2** | Stores actual image files (bytes). Object storage like AWS S3. |
| **PostgreSQL** | Stores structured data: users, image metadata, relationships. |

R2 is **not** a database replacement - it's blob storage for files. PostgreSQL handles everything else.

### Upload Flow
1. Frontend requests presigned PUT URL from backend
2. Frontend uploads directly to R2 using presigned URL (PUT request)
3. Frontend calls confirm endpoint with file metadata
4. Backend verifies file exists in R2 (HEAD request), then saves metadata to PostgreSQL

---

## Project Structure
```
image_hosting/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app + CORS + lifespan
│   │   ├── config.py            # Settings from .env (pydantic-settings)
│   │   ├── database.py          # SQLAlchemy engine + session
│   │   ├── dependencies.py      # Auth dependency, DB session
│   │   │
│   │   ├── models/              # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # User table
│   │   │   └── image.py         # Image metadata table
│   │   │
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # UserCreate, UserResponse, etc.
│   │   │   ├── image.py         # ImageUpload, ImageResponse, etc.
│   │   │   └── auth.py          # LoginRequest, TokenResponse
│   │   │
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Register, login, /me
│   │   │   └── images.py        # Upload, list, delete
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Password hashing, JWT
│   │   │   └── storage.py       # R2 via boto3
│   │   │
│   │   └── logging.py           # Loguru configuration
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Fixtures, test DB setup
│   │   ├── unit/
│   │   │   ├── test_auth.py
│   │   │   └── test_storage.py
│   │   └── integration/
│   │       ├── test_api_auth.py
│   │       └── test_api_images.py
│   │
│   ├── pyproject.toml           # uv project config
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx              # Routing
│   │   ├── api/client.ts        # Axios with auth interceptor
│   │   ├── context/AuthContext.tsx
│   │   ├── components/
│   │   │   ├── DropZone.tsx
│   │   │   ├── ImageGallery.tsx
│   │   │   ├── ImageCard.tsx
│   │   │   ├── CopyButton.tsx
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   └── RegisterPage.tsx
│   │   ├── hooks/
│   │   │   └── useImages.ts
│   │   └── types/
│   │       ├── auth.ts
│   │       └── image.ts
│   │
│   ├── tests/
│   │   ├── setup.ts             # Vitest setup
│   │   ├── components/
│   │   │   ├── DropZone.test.tsx
│   │   │   └── ImageCard.test.tsx
│   │   └── pages/
│   │       └── HomePage.test.tsx
│   │
│   ├── package.json
│   ├── vite.config.ts
│   ├── vitest.config.ts
│   ├── tailwind.config.js
│   ├── .env.example
│   └── Dockerfile
│
├── docker-compose.yml           # Backend + Frontend + PostgreSQL
├── docs/
│   └── mockups/                 # UI/UX wireframes and user flows
│       ├── 01-login-page.md
│       ├── 02-register-page.md
│       ├── 03-home-gallery.md
│       ├── 04-image-card.md
│       └── 05-user-flows.md
├── .gitignore
└── README.md
```

---

## Data Models

### SQLAlchemy ORM Models (backend/app/models/)

```python
# models/user.py
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    images: Mapped[list["Image"]] = relationship(back_populates="user")

# models/image.py
class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    filename: Mapped[str] = mapped_column(String(255))
    r2_key: Mapped[str] = mapped_column(String(500), unique=True)  # path in R2
    content_type: Mapped[str] = mapped_column(String(100))
    size_bytes: Mapped[int] = mapped_column()
    public_url: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    user: Mapped["User"] = relationship(back_populates="images")
```

### Async Database Setup (backend/app/database.py)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@db:5432/imagehosting",
    echo=False,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session
```

### FastAPI Lifespan (backend/app/main.py)

> **Note**: Use `lifespan` context manager instead of deprecated `@app.on_event("startup")`.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables, initialize connections
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: cleanup
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

### Pydantic Schemas (backend/app/schemas/)

```python
# schemas/user.py
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# schemas/auth.py
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# schemas/image.py
class ImageUploadRequest(BaseModel):
    filename: str
    content_type: str = Field(pattern=r"^image/")

class ImageUploadResponse(BaseModel):
    upload_url: str      # Presigned R2 URL
    r2_key: str
    public_url: str

class ImageResponse(BaseModel):
    id: int
    filename: str
    public_url: str
    size_bytes: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ImageListResponse(BaseModel):
    images: list[ImageResponse]
    total: int
```

---

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

---

## R2 Storage Service Pattern

### Presigned PUT URL (backend/app/services/storage.py)

> **Note**: Use PUT presigned URLs for simpler frontend uploads (no multipart form needed).

```python
import boto3
from botocore.config import Config

class R2Storage:
    def __init__(self, account_id: str, access_key: str, secret_key: str, bucket: str):
        self.bucket = bucket
        self.client = boto3.client(
            "s3",
            endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
        )

    def generate_upload_url(self, key: str, content_type: str, expires_in: int = 3600) -> str:
        """Generate presigned PUT URL for direct upload."""
        return self.client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )

    def verify_object_exists(self, key: str) -> dict | None:
        """Verify upload succeeded before saving metadata. Returns object info or None."""
        try:
            response = self.client.head_object(Bucket=self.bucket, Key=key)
            return {"size": response["ContentLength"], "content_type": response["ContentType"]}
        except self.client.exceptions.ClientError:
            return None

    def delete_object(self, key: str) -> bool:
        """Delete object from R2."""
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            return True
        except self.client.exceptions.ClientError:
            return False
```

### Frontend Upload (simplified PUT)

```typescript
// Upload directly to R2 with presigned URL
const uploadToR2 = async (file: File, presignedUrl: string) => {
  const response = await fetch(presignedUrl, {
    method: "PUT",
    body: file,
    headers: {
      "Content-Type": file.type,
    },
  });
  return response.ok;
};
```

---

## Key Dependencies

### Backend (pyproject.toml with uv)
```toml
[project]
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "sqlalchemy>=2.0.0",
    "asyncpg>=0.29.0",           # Async PostgreSQL driver
    "alembic>=1.13.0",           # Database migrations
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "python-jose[cryptography]>=3.3.0",  # JWT
    "passlib[bcrypt]>=1.7.4",    # Password hashing
    "boto3>=1.34.0",             # R2/S3 client
    "loguru>=0.7.0",             # Logging
    "python-multipart>=0.0.6",   # Form data
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.26.0",             # Test client
    "pytest-vcr>=1.0.0",         # Record/replay HTTP
]
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.22.0",
    "axios": "^1.6.0",
    "react-dropzone": "^14.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.1.0",
    "tailwindcss": "^3.4.0",
    "vitest": "^1.2.0",
    "@testing-library/react": "^14.2.0",
    "@testing-library/jest-dom": "^6.4.0"
  }
}
```

---

## Validation & Security

### File Upload Validation

**Frontend validation (immediate feedback):**
- Max file size: 10MB
- Allowed types: `image/jpeg`, `image/png`, `image/gif`, `image/webp`
- Validate before requesting presigned URL

**Backend validation:**
- Verify content-type matches allowed image types
- Generate unique R2 key with UUID to prevent overwrites
- Verify file exists in R2 before saving metadata (prevents orphaned DB records)

```python
# schemas/image.py - with validation
class ImageUploadRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(pattern=r"^image/(jpeg|png|gif|webp)$")
    size_bytes: int = Field(gt=0, le=10_485_760)  # Max 10MB
```

### Security Considerations

- **R2 key generation**: Use `{user_id}/{uuid}.{ext}` pattern to namespace by user
- **Confirm endpoint**: Always verify file exists in R2 before saving to DB
- **Delete cascade**: Delete from R2 first, then DB (if R2 fails, don't delete DB record)
- **JWT validation**: Verify token on every authenticated request
- **CORS**: Restrict to frontend origin only

---

## Implementation Steps

### Phase 1: Project Setup (Steps 1-5)
1. Create backend directory structure with `uv init`
2. Initialize Vite React TypeScript project
3. Install and configure Tailwind CSS
4. Create Docker Compose configuration (backend, frontend, postgres)
5. Create `.env.example` files and `.gitignore`

### Phase 2: UI/UX Design (Steps 6-8)
6. Create wireframe mockups for all pages (ASCII/text-based in `docs/mockups/`)
7. Define user flows: registration, login, upload, gallery browse, copy URL, delete
8. Document component hierarchy and state management approach

**Mockups to create:**
- `docs/mockups/01-login-page.md` - Login form layout
- `docs/mockups/02-register-page.md` - Registration form layout
- `docs/mockups/03-home-gallery.md` - Main gallery with upload dropzone
- `docs/mockups/04-image-card.md` - Individual image card with actions
- `docs/mockups/05-user-flows.md` - User journey diagrams

### Phase 3: Database & Models (Steps 9-12)
9. Configure async SQLAlchemy with `create_async_engine` and `async_sessionmaker` (`database.py`)
10. Define SQLAlchemy ORM models with `Mapped` type hints (`models/user.py`, `models/image.py`)
11. Define Pydantic schemas with validation constraints (`schemas/`)
12. Set up Alembic for async database migrations

### Phase 4: Backend - Auth (Steps 13-16)
13. Implement `config.py` with pydantic-settings
14. Configure Loguru logging (`logging.py`) with LOG_LEVEL env var
15. Implement auth service (password hashing, JWT)
16. Create auth router (register, login, /me)

### Phase 5: Backend - Storage (Steps 17-19)
17. Implement R2 storage service with presigned PUT URLs and verification
18. Create images router (upload-url, confirm with R2 verification, list, delete)
19. Wire up routers in `main.py` with lifespan, CORS, and logging middleware

### Phase 6: Backend - Testing (Steps 20-22)
20. Set up pytest with fixtures and test database
21. Write unit tests for auth and storage services
22. Write integration tests for API endpoints (with VCR for R2)

### Phase 7: Frontend - Core (Steps 23-26)
23. Create `api/client.ts` with axios + auth interceptor
24. Implement `AuthContext.tsx` for auth state
25. Set up React Router in `App.tsx`
26. Create ErrorBoundary component

### Phase 8: Frontend - Features (Steps 27-31)
27. Build LoginForm and RegisterForm components
28. Build `DropZone.tsx` with react-dropzone (include size/type validation)
29. Create `ImageGallery.tsx` and `ImageCard.tsx`
30. Implement `CopyButton.tsx` with clipboard API
31. Style with Tailwind (responsive grid, forms, buttons)

### Phase 9: Frontend - Testing (Steps 32-33)
32. Configure Vitest with React Testing Library
33. Write component tests (DropZone, ImageCard, forms)

### Phase 10: Integration & Polish (Steps 34-36)
34. Test Docker Compose full stack locally
35. Create Cloudflare R2 bucket + API credentials
36. End-to-end test: register → login → upload → view → copy → delete

### Phase 11: Documentation & Code Quality (Optional)
37. Add structured docstrings (Google style) to all Python modules, classes, and functions
38. Add JSDoc comments to TypeScript functions and components
39. Generate API documentation (e.g., Sphinx for backend, TypeDoc for frontend)
40. Review and improve type hint coverage (run mypy/pyright)

---

## Environment Variables

### Backend `.env`
```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/imagehosting

# JWT
JWT_SECRET_KEY=generate-a-32-char-minimum-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=10080  # 7 days

# Cloudflare R2
R2_ACCOUNT_ID=your_cloudflare_account_id
R2_ACCESS_KEY_ID=your_r2_access_key
R2_SECRET_ACCESS_KEY=your_r2_secret_key
R2_BUCKET_NAME=image-hosting
R2_PUBLIC_URL=https://pub-xxx.r2.dev

# Logging
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR

# App
FRONTEND_URL=http://localhost:5173
```

### Frontend `.env`
```bash
VITE_API_URL=http://localhost:8000/api
```

---

## Docker Compose Configuration

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: imagehosting
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/imagehosting
    env_file:
      - ./backend/.env
    depends_on:
      - db
    volumes:
      - ./backend:/app  # Dev: hot reload

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    env_file:
      - ./frontend/.env
    depends_on:
      - backend
    volumes:
      - ./frontend:/app  # Dev: hot reload
      - /app/node_modules

volumes:
  postgres_data:
```

---

## Testing Strategy

### Backend (pytest)
```bash
# Run all tests with coverage
uv run pytest --cov=app --cov-report=html

# Run only unit tests
uv run pytest tests/unit/

# Run only integration tests
uv run pytest tests/integration/
```

**Unit tests**: Test services in isolation (mock DB, mock R2)
**Integration tests**: Test full API endpoints with test database

### Frontend (Vitest)
```bash
# Run tests
npm run test

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

---

## Verification Plan
1. `docker-compose up --build` - Start all services
2. Check backend logs: should see Loguru output at DEBUG level
3. `curl http://localhost:8000/api/health` - Health check
4. Register: POST to `/api/auth/register`
5. Login: POST to `/api/auth/login` → get JWT
6. Upload: Get presigned URL → PUT image to R2 → confirm
7. Gallery: GET `/api/images/` → see uploaded images
8. Copy URL: Paste in browser → image loads
9. Delete: DELETE `/api/images/{id}` → removed from DB and R2
10. Run test suites: `uv run pytest` and `npm run test`
