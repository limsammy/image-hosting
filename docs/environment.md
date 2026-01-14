# Environment Variables

Complete reference for all configuration options.

## Backend (`backend/.env`)

### Database

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string with asyncpg driver |

**Format**: `postgresql+asyncpg://user:password@host:port/database`

**Examples**:
```bash
# Docker Compose
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/imagehosting

# Local PostgreSQL
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/imagehosting
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
| `R2_ACCESS_KEY_ID` | Yes | - | R2 API token access key |
| `R2_SECRET_ACCESS_KEY` | Yes | - | R2 API token secret key |
| `R2_BUCKET_NAME` | Yes | - | Name of your R2 bucket |
| `R2_PUBLIC_URL` | Yes | - | Public URL for serving images |

**Finding your Account ID**:
1. Log in to Cloudflare Dashboard
2. Go to R2 section
3. Account ID is in the URL or sidebar

**Creating R2 API Token**:
1. Go to R2 → Manage R2 API Tokens
2. Create token with "Object Read & Write" permission
3. Copy Access Key ID and Secret Access Key

**Public URL formats**:
```bash
# R2.dev subdomain (free)
R2_PUBLIC_URL=https://pub-xxxxxxxxxxxx.r2.dev

# Custom domain (requires setup)
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

**backend/.env**:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/imagehosting
JWT_SECRET_KEY=dev-secret-key-change-in-production-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=10080
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=image-hosting-dev
R2_PUBLIC_URL=https://pub-xxx.r2.dev
LOG_LEVEL=DEBUG
FRONTEND_URL=http://localhost:5173
```

**frontend/.env**:
```bash
VITE_API_URL=http://localhost:8000/api
```

### Production

**backend/.env**:
```bash
DATABASE_URL=postgresql+asyncpg://produser:strongpassword@db.example.com:5432/imagehosting
JWT_SECRET_KEY=<generated-32-char-secret>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=image-hosting-prod
R2_PUBLIC_URL=https://images.yourdomain.com
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
