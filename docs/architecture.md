# Architecture

System design and architectural decisions for the Image Hosting App.

## System Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │────▶│   Frontend  │────▶│   Backend   │
│             │     │  (React)    │     │  (FastAPI)  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                          ┌────────────────────┼────────────────────┐
                          │                    │                    │
                          ▼                    ▼                    ▼
                    ┌───────────┐        ┌───────────┐        ┌───────────┐
                    │ PostgreSQL│        │Cloudflare │        │   JWT     │
                    │ (metadata)│        │    R2     │        │  (auth)   │
                    └───────────┘        │ (images)  │        └───────────┘
                                         └───────────┘
```

## Component Responsibilities

### Frontend (React + TypeScript)

- User interface and interactions
- Form validation (client-side)
- Direct uploads to R2 via presigned URLs
- JWT token management (localStorage)
- Responsive design with Tailwind

### Backend (FastAPI + Python)

- REST API endpoints
- Authentication (JWT generation/validation)
- Authorization (user can only access own images)
- Presigned URL generation for R2
- Database operations (SQLAlchemy)
- Request validation (Pydantic)

### PostgreSQL

- User accounts (credentials, profile)
- Image metadata (filename, R2 key, timestamps)
- Relationships (user → images)

### Cloudflare R2

- Actual image file storage (bytes)
- Direct browser uploads via presigned URLs
- Public URLs for serving images

## Data Flow

### Image Upload Flow

```
1. User selects file in browser
   │
2. Frontend validates (size, type)
   │
3. Frontend requests presigned URL
   │  POST /api/images/upload-url
   │  Body: { filename, content_type, size_bytes }
   │
4. Backend generates presigned PUT URL
   │  - Validates content type
   │  - Generates unique R2 key: {user_id}/{uuid}.{ext}
   │  - Returns: { upload_url, r2_key, public_url }
   │
5. Frontend uploads directly to R2
   │  PUT {presigned_url}
   │  Body: file bytes
   │
6. Frontend confirms upload
   │  POST /api/images/confirm
   │  Body: { r2_key, filename, size_bytes }
   │
7. Backend verifies file exists in R2
   │  HEAD request to R2
   │
8. Backend saves metadata to PostgreSQL
   │
9. Frontend displays image in gallery
```

### Authentication Flow

```
1. User submits credentials
   │  POST /api/auth/login
   │
2. Backend validates password (bcrypt)
   │
3. Backend generates JWT (7-day expiry)
   │
4. Frontend stores token in localStorage
   │
5. All subsequent requests include:
   │  Authorization: Bearer {token}
   │
6. Backend validates token on each request
```

## Design Decisions

### Why Presigned URLs for Uploads?

**Decision**: Frontend uploads directly to R2, not through backend.

**Rationale**:
- Reduces backend bandwidth and memory usage
- Faster uploads (direct to CDN edge)
- Backend only handles metadata, not file bytes
- Scales better with many concurrent uploads

**Trade-off**: More complex client code, but worth it for performance.

### Why Separate R2 and PostgreSQL?

**Decision**: Store files in R2, metadata in PostgreSQL.

**Rationale**:
- R2 is optimized for blob storage (S3-compatible)
- PostgreSQL is optimized for structured queries
- Can query images by date, user, etc. without scanning files
- R2 has unlimited free egress (serving images)

### Why JWT Instead of Sessions?

**Decision**: Stateless JWT tokens for authentication.

**Rationale**:
- No server-side session storage needed
- Works well with stateless backend containers
- Easy to scale horizontally
- Frontend can decode token for user info

**Trade-off**: Can't invalidate tokens before expiry (acceptable for this app).

### Why SQLAlchemy 2.0 Async?

**Decision**: Use async SQLAlchemy with asyncpg driver.

**Rationale**:
- FastAPI is async-native
- Better performance under concurrent load
- Non-blocking database operations
- Consistent async/await pattern throughout

### Why Tailwind CSS?

**Decision**: Utility-first CSS with Tailwind.

**Rationale**:
- No context-switching between CSS and components
- Consistent design system out of the box
- Small bundle size (only used classes)
- Rapid prototyping

## Security Considerations

### Input Validation

- **Backend**: Pydantic validates all request bodies
- **Frontend**: Validates before sending requests
- **File uploads**: Validated by content type, size, and R2 key pattern

### Authentication

- Passwords hashed with bcrypt (cost factor 12)
- JWT signed with HS256 algorithm
- Token expiry: 7 days
- Tokens stored in localStorage (acceptable for this app)

### Authorization

- Users can only access their own images
- R2 keys namespaced by user ID: `{user_id}/{uuid}.{ext}`
- Backend verifies ownership on all operations

### CORS

- Frontend origin explicitly allowed
- Credentials included for authenticated requests
- No wildcard origins in production

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Images table
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    filename VARCHAR(255) NOT NULL,
    r2_key VARCHAR(500) UNIQUE NOT NULL,
    content_type VARCHAR(100) NOT NULL,
    size_bytes INTEGER NOT NULL,
    public_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for user's images
CREATE INDEX idx_images_user_id ON images(user_id);
```

## API Design

### REST Conventions

- All endpoints prefixed with `/api/`
- JSON request/response bodies
- HTTP status codes: 200/201 (success), 400 (validation), 401 (auth), 404 (not found)
- Consistent error response format

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Get JWT token |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/images/upload-url` | Get presigned URL |
| POST | `/api/images/confirm` | Confirm upload |
| GET | `/api/images/` | List user's images |
| DELETE | `/api/images/{id}` | Delete image |
| GET | `/api/health` | Health check |

## Future Considerations

### Potential Enhancements

- **Image processing**: Thumbnail generation, resizing
- **Rate limiting**: Prevent abuse of upload endpoints
- **Caching**: Redis for session/token caching
- **CDN**: Cloudflare CDN in front of R2
- **Monitoring**: Prometheus metrics, structured logging

### Scaling Strategy

- Backend: Horizontal scaling with load balancer
- Database: Read replicas, connection pooling
- Storage: R2 scales automatically
- Frontend: CDN-hosted static build
