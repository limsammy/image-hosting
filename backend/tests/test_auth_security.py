"""
Security tests for authentication endpoints.

Tests to ensure sensitive fields are not exposed in API responses.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth_me_does_not_expose_is_admin(client: AsyncClient, admin_auth_headers):
    """
    Verify that /api/auth/me does NOT expose the is_admin field.

    Security: is_admin should only be used internally for authorization,
    never exposed to clients (even to admin users themselves).
    """
    response = await client.get("/api/auth/me", headers=admin_auth_headers)

    assert response.status_code == 200
    data = response.json()

    # Verify is_admin is NOT in the response
    assert "is_admin" not in data, "is_admin field should not be exposed in /api/auth/me"

    # Verify only expected fields are present
    expected_fields = {"id", "username", "email", "created_at"}
    actual_fields = set(data.keys())

    assert actual_fields == expected_fields, (
        f"Unexpected fields in response. Expected: {expected_fields}, Got: {actual_fields}"
    )


@pytest.mark.asyncio
async def test_register_does_not_expose_is_admin(client: AsyncClient):
    """
    Verify that /api/auth/register does NOT expose the is_admin field.

    Security: Newly registered users should not see is_admin in the response.
    """
    response = await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 201
    data = response.json()

    # Verify is_admin is NOT in the response
    assert "is_admin" not in data, "is_admin field should not be exposed in /api/auth/register"

    # Verify only expected fields are present
    expected_fields = {"id", "username", "email", "created_at"}
    actual_fields = set(data.keys())

    assert actual_fields == expected_fields, (
        f"Unexpected fields in response. Expected: {expected_fields}, Got: {actual_fields}"
    )
