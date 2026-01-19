# Image Hosting App

A minimalist image hosting service with drag-and-drop uploads, user authentication, and Cloudflare R2 storage.

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, SQLAlchemy, PostgreSQL, Pydantic |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS |
| **Storage** | Cloudflare R2 (S3-compatible) |
| **Auth** | JWT tokens with bcrypt password hashing |

## Project Structure

```
image_hosting/
├── backend/           # FastAPI Python backend
│   ├── app/
│   │   ├── models/    # SQLAlchemy ORM models
│   │   ├── schemas/   # Pydantic request/response schemas
│   │   ├── routers/   # API route handlers
│   │   └── services/  # Business logic (auth, storage)
│   └── tests/
├── frontend/          # React TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/    # Design system (tokens.css, components.css)
│   │   └── hooks/
│   └── tests/
└── docs/
```

## Quick Commands

```bash
# Start frontend dev server
cd frontend && npm run dev

# Build frontend
cd frontend && npm run build

# Backend
cd backend && uv run uvicorn app.main:app --reload

# Run tests (use 30s timeout - pytest may appear to hang after completion)
cd backend && uv run pytest -q
```

## Known Issues

**Pytest hangs after completion**: When running pytest, it may appear to run indefinitely even after showing test results. Always use a short timeout (30s) when running tests. If tests pass but the command doesn't exit, the tests succeeded.

## MCP Tools - Use Selectively

**Default: Use built-in Claude Code tools** (Read, Edit, Write, Grep, Glob, Bash). These are fast, have no overhead, and handle 90% of tasks.

### When to Use MCP Tools

| Tool | Use When | Don't Use When |
|------|----------|----------------|
| **Serena** | Complex refactoring across many files, need to find all references to a symbol, exploring unfamiliar large codebase | Simple file edits, reading 1-3 files, small projects |
| **Context7** | Need current API docs for a library (FastAPI, React, etc.), unsure about library patterns | You already know the API, making simple changes |
| **Sequential Thinking** | Genuinely complex multi-step problem, debugging tricky issues, architectural decisions with many trade-offs | Routine coding tasks, simple bug fixes, straightforward implementations |

### Serena Activation (Only When Needed)

```
mcp__serena__activate_project with path: /Users/sam/projects/image_hosting
```

Useful Serena commands:
- `find_symbol` - Find a class/function by name
- `find_referencing_symbols` - Find all usages of a symbol
- `get_symbols_overview` - Overview of symbols in a file

### Context7 (Only When Needed)

```
mcp__context7__resolve-library-id  # Find library ID
mcp__context7__query-docs          # Query for specific help
```

## Implementation Status

See [PLAN.md](./PLAN.md) for full plan.

**Completed:**
- Phase 1: Project setup (backend, frontend, Docker, docs)
- Phase 2: UI/UX mockups and design system
- Phase 3: Database models (User, Image) with Alembic migrations

**Current:** Phase 4 - Auth & Storage services
