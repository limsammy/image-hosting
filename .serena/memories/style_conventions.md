# Code Style and Conventions

## Backend (Python)

### General Style
- Use async/await for all database and HTTP operations
- Pydantic models for all request/response validation
- SQLAlchemy 2.0 style with `Mapped` type hints
- Loguru for all logging (not stdlib logging)

### Type Hints
- Always use type hints for function parameters and return types
- Use `Mapped[]` for SQLAlchemy ORM model columns
- Use Pydantic `Field()` for validation constraints

### SQLAlchemy Models Example
```python
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
```

### Pydantic Schemas Example
```python
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)
```

## Frontend (TypeScript)

### General Style
- Functional components with hooks (no class components)
- Context API for global state (auth)
- Axios for API calls with interceptors
- Tailwind for styling (no separate CSS files)

### Component Structure
- Place components in `src/components/`
- Place page components in `src/pages/`
- Place hooks in `src/hooks/`
- Place context providers in `src/context/`
- Place TypeScript types in `src/types/`

### Naming Conventions
- PascalCase for component files and names (e.g., `DropZone.tsx`)
- camelCase for hooks (e.g., `useImages.ts`)
- camelCase for utility functions
- Use `.tsx` for React components, `.ts` for plain TypeScript

## API Conventions
- All endpoints prefixed with `/api/`
- Use JWT Bearer tokens for authentication
- Content-Type: application/json for all requests
- Consistent error response format
