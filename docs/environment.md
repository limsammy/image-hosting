# Environment Variables

Complete reference for all configuration options.

## Backend (`backend/.env`)

### Database

The database can be configured either with individual variables (recommended for local dev) or a connection URL.

**Option A: Individual Variables (Local Development)**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `POSTGRES_HOST` | Yes | - | Database hostname |
| `POSTGRES_PORT` | No | `5432` | Database port |
| `POSTGRES_USER` | Yes | - | Database username |
| `POSTGRES_PASSWORD` | Yes | - | Database password |
| `POSTGRES_DB` | Yes | - | Database name |
| `POSTGRES_DB_DEV` | No | `imagehosting_dev` | Development database name (for reference) |

**Example** (using `./scripts/setup-local-db.sh`):
```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=imagehosting_user
POSTGRES_PASSWORD=imagehosting_dev_password
POSTGRES_DB=imagehosting_dev
POSTGRES_DB_DEV=imagehosting_dev
```

**Note:** Tests use an in-memory SQLite database - no PostgreSQL test database is needed.

**Option B: Connection URL**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | No | - | Full PostgreSQL connection string (overrides individual vars) |

**Format**: `postgresql+asyncpg://user:password@host:port/database`

```bash
# Docker Compose (set automatically)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/imagehosting
```

### Authentication

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JWT_SECRET_KEY` | Yes | - | Secret key for signing JWT tokens (min 32 chars) |
| `JWT_ALGORITHM` | No | `HS256` | Algorithm for JWT signing |
| `JWT_EXPIRATION_MINUTES` | No | `10080` | Token expiry in minutes (default: 7 days) |

**Generating a secret key**:
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32
```

### Cloudflare R2

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `R2_ACCOUNT_ID` | Yes | - | Your Cloudflare account ID |
| `R2_ACCESS_KEY` | Yes | - | R2 API token access key |
| `R2_SECRET_KEY` | Yes | - | R2 API token secret key |
| `R2_BUCKET_NAME` | Yes | `image-hosting` | Name of your R2 bucket |
| `R2_PUBLIC_URL` | Yes | - | Public URL for serving images |
| `R2_TOKEN` | No | - | R2 API token (for reference) |
| `R2_JURISDICTION_URL` | No | - | Custom S3 endpoint (optional) |

**Finding your Account ID**:
1. Log in to Cloudflare Dashboard
2. Go to R2 section
3. Account ID is in the URL: `dash.cloudflare.com/<ACCOUNT_ID>/r2`

**Creating R2 API Token**:
1. Go to R2 → Manage R2 API Tokens
2. Create token with "Object Read & Write" permission
3. Scope to specific bucket (e.g., `image-hosting`)
4. Copy Access Key ID and Secret Access Key (shown only once)

**Public URL formats**:
```bash
# R2.dev subdomain (free, auto-generated)
R2_PUBLIC_URL=https://pub-xxxxxxxxxxxx.r2.dev

# Custom domain (requires Cloudflare DNS setup)
R2_PUBLIC_URL=https://images.yourdomain.com
```

### Logging

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LOG_LEVEL` | No | `INFO` | Logging verbosity |

**Valid values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

**Recommendations**:
- Development: `DEBUG`
- Production: `INFO` or `WARNING`

### Application

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FRONTEND_URL` | Yes | - | Frontend origin for CORS |

**Examples**:
```bash
# Local development
FRONTEND_URL=http://localhost:5173

# Production
FRONTEND_URL=https://images.yourdomain.com
```

## Frontend (`frontend/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_URL` | Yes | - | Backend API base URL |

**Examples**:
```bash
# Local development
VITE_API_URL=http://localhost:8000/api

# Production
VITE_API_URL=https://api.yourdomain.com/api
```

**Note**: All Vite environment variables must be prefixed with `VITE_` to be exposed to the client.

## Docker Compose Overrides

Docker Compose can override environment variables. The `docker-compose.yml` sets:

```yaml
environment:
  - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/imagehosting
```

This overrides any `DATABASE_URL` in `backend/.env` to use the Docker network hostname `db`.

## Example Configurations

### Local Development

**backend/.env** (after running `./scripts/setup-local-db.sh`):
```bash
# Database (local PostgreSQL)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=imagehosting_user
POSTGRES_PASSWORD=imagehosting_dev_password
POSTGRES_DB=imagehosting_dev
POSTGRES_DB_DEV=imagehosting_dev

# Auth
JWT_SECRET_KEY=dev-secret-key-change-in-production-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=10080

# Cloudflare R2
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY=your_access_key
R2_SECRET_KEY=your_secret_key
R2_BUCKET_NAME=image-hosting
R2_PUBLIC_URL=https://pub-xxx.r2.dev

# App
LOG_LEVEL=DEBUG
FRONTEND_URL=http://localhost:5173
```

**frontend/.env**:
```bash
VITE_API_URL=http://localhost:8000/api
```

### Docker Development

When using `docker-compose up`, the `POSTGRES_HOST` is overridden to `db` automatically.

### Production

**backend/.env**:
```bash
# Database
POSTGRES_HOST=db.example.com
POSTGRES_PORT=5432
POSTGRES_USER=produser
POSTGRES_PASSWORD=strongpassword
POSTGRES_DB=imagehosting

# Auth
JWT_SECRET_KEY=<generated-32-char-secret>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Cloudflare R2
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY=your_access_key
R2_SECRET_KEY=your_secret_key
R2_BUCKET_NAME=image-hosting
R2_PUBLIC_URL=https://images.yourdomain.com

# App
LOG_LEVEL=WARNING
FRONTEND_URL=https://yourdomain.com
```

**frontend/.env**:
```bash
VITE_API_URL=https://api.yourdomain.com/api
```

## Security Notes

1. **Never commit `.env` files** - They're in `.gitignore`
2. **Use strong secrets** - Generate random keys for production
3. **Rotate credentials** - Periodically update R2 API tokens
4. **Restrict CORS** - Only allow your frontend origin
5. **Use HTTPS** - In production, all URLs should be HTTPS
