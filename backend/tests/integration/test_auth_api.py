"""
Integration tests for auth API endpoints.
"""

import pytest
from httpx import AsyncClient


class TestRegister:
    """Tests for POST /api/auth/register endpoint."""

    async def test_register_success(self, client: AsyncClient):
        """Should register a new user successfully."""
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data
        assert "password_hash" not in data

    async def test_register_duplicate_username(self, client: AsyncClient):
        """Should reject duplicate username."""
        # Register first user
        await client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test1@example.com",
                "password": "password123",
            },
        )
        # Try to register with same username
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test2@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]

    async def test_register_duplicate_email(self, client: AsyncClient):
        """Should reject duplicate email."""
        # Register first user
        await client.post(
            "/api/auth/register",
            json={
                "username": "user1",
                "email": "same@example.com",
                "password": "password123",
            },
        )
        # Try to register with same email
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "user2",
                "email": "same@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    async def test_register_invalid_email(self, client: AsyncClient):
        """Should reject invalid email format."""
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "not-an-email",
                "password": "password123",
            },
        )
        assert response.status_code == 422

    async def test_register_short_password(self, client: AsyncClient):
        """Should reject short passwords."""
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "short",
            },
        )
        assert response.status_code == 422


class TestLogin:
    """Tests for POST /api/auth/login endpoint."""

    async def test_login_success_with_username(self, client: AsyncClient):
        """Should login with correct username and password."""
        # Register user first
        await client.post(
            "/api/auth/register",
            json={
                "username": "loginuser",
                "email": "login@example.com",
                "password": "password123",
            },
        )
        # Login
        response = await client.post(
            "/api/auth/login",
            data={"username": "loginuser", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_success_with_email(self, client: AsyncClient):
        """Should login with email instead of username."""
        # Register user first
        await client.post(
            "/api/auth/register",
            json={
                "username": "emailuser",
                "email": "email@example.com",
                "password": "password123",
            },
        )
        # Login with email
        response = await client.post(
            "/api/auth/login",
            data={"username": "email@example.com", "password": "password123"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    async def test_login_wrong_password(self, client: AsyncClient):
        """Should reject wrong password."""
        # Register user first
        await client.post(
            "/api/auth/register",
            json={
                "username": "wrongpw",
                "email": "wrongpw@example.com",
                "password": "password123",
            },
        )
        # Login with wrong password
        response = await client.post(
            "/api/auth/login",
            data={"username": "wrongpw", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Should reject nonexistent user."""
        response = await client.post(
            "/api/auth/login",
            data={"username": "doesnotexist", "password": "password123"},
        )
        assert response.status_code == 401


class TestMe:
    """Tests for GET /api/auth/me endpoint."""

    async def test_me_authenticated(self, client: AsyncClient):
        """Should return current user info when authenticated."""
        # Register and login
        await client.post(
            "/api/auth/register",
            json={
                "username": "meuser",
                "email": "me@example.com",
                "password": "password123",
            },
        )
        login_response = await client.post(
            "/api/auth/login",
            data={"username": "meuser", "password": "password123"},
        )
        token = login_response.json()["access_token"]

        # Get current user
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "meuser"
        assert data["email"] == "me@example.com"

    async def test_me_unauthenticated(self, client: AsyncClient):
        """Should reject request without token."""
        response = await client.get("/api/auth/me")
        assert response.status_code == 401

    async def test_me_invalid_token(self, client: AsyncClient):
        """Should reject invalid token."""
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert response.status_code == 401
