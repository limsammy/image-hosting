"""
Pytest fixtures for testing.

Uses in-memory SQLite for fast test execution.
No external database setup required.
"""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import Base, get_session
from app.main import app


# In-memory SQLite database for testing (fast, no setup required)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with database session override."""

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def admin_user(session: AsyncSession):
    """Create an admin user for testing."""
    from app.models import User
    from app.services.auth import AuthService

    user = User(
        username="admin",
        email="admin@example.com",
        password_hash=AuthService.hash_password("adminpassword"),
        is_admin=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture
async def admin_auth_headers(admin_user):
    """Get auth headers for admin user."""
    from app.services.auth import AuthService

    token = AuthService.create_access_token(admin_user.id)
    return {"Authorization": f"Bearer {token}"}
