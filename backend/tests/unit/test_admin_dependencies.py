"""
Unit tests for admin authorization dependencies.

Tests the require_admin dependency that protects admin-only endpoints.
"""

import pytest
from fastapi import HTTPException

from app.dependencies import require_admin
from app.models import User


@pytest.mark.asyncio
async def test_require_admin_allows_admin_user():
    """Verify require_admin allows users with is_admin=True."""
    admin_user = User(
        id=1,
        username="admin",
        email="admin@example.com",
        password_hash="hashed",
        is_admin=True,
    )

    # Should not raise exception
    result = await require_admin(admin_user)
    assert result == admin_user


@pytest.mark.asyncio
async def test_require_admin_blocks_regular_user():
    """Verify require_admin blocks users with is_admin=False."""
    regular_user = User(
        id=2,
        username="user",
        email="user@example.com",
        password_hash="hashed",
        is_admin=False,
    )

    # Should raise 403 Forbidden
    with pytest.raises(HTTPException) as exc_info:
        await require_admin(regular_user)

    assert exc_info.value.status_code == 403
    assert "admin privileges" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_require_admin_blocks_none_is_admin():
    """Verify require_admin blocks users where is_admin is None (legacy data)."""
    legacy_user = User(
        id=3,
        username="legacy",
        email="legacy@example.com",
        password_hash="hashed",
        is_admin=None,  # Legacy user without is_admin set
    )

    # Should raise 403 Forbidden (treat None as False)
    with pytest.raises(HTTPException) as exc_info:
        await require_admin(legacy_user)

    assert exc_info.value.status_code == 403
