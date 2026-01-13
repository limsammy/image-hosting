# Image Hosting App

A minimalist image hosting service with drag-and-drop uploads, user authentication, and Cloudflare R2 storage.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Pydantic
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS
- **Storage**: Cloudflare R2 (S3-compatible)
- **Auth**: JWT tokens with bcrypt password hashing

## MCP Tools Workflow

### 1. Serena (Semantic Code Navigation)

Activate at the start of each session:
```
mcp__serena__activate_project with path: /Users/sam/projects/image_hosting
```

Then read project memories for context:
```
mcp__serena__list_memories
mcp__serena__read_memory
```

Use Serena for:
- **Code exploration**: `get_symbols_overview`, `find_symbol`, `find_referencing_symbols`
- **Code editing**: `replace_symbol_body`, `insert_after_symbol`, `insert_before_symbol`
- **Search**: `search_for_pattern`, `find_file`, `list_dir`

Prefer Serena's symbolic tools over reading entire files when possible.

### 2. Context7 (Library Documentation)

Use for up-to-date documentation on any library:
```
mcp__context7__resolve-library-id  # Find the library ID first
mcp__context7__query-docs          # Then query for specific help
```

Useful for: FastAPI, SQLAlchemy, React, Tailwind, boto3, Pydantic, etc.

### 3. Sequential Thinking (Complex Problems)

Use `mcp__sequential-thinking__sequentialthinking` when:
- Breaking down complex multi-step implementations
- Debugging tricky issues that need step-by-step analysis
- Planning architectural decisions with trade-offs
- Problems where the full scope isn't clear initially

## Implementation Plan

See [PLAN.md](./PLAN.md) for the full implementation plan (10 phases, 36 steps).

## Current Status

**Not started** - No code has been implemented yet.
