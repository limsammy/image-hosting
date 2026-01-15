"""
Unit tests for AuthService.
"""

import pytest

from app.services.auth import AuthService


class TestPasswordHashing:
    """Tests for password hashing functionality."""

    def test_hash_password_returns_different_value(self):
        """Hashed password should differ from plain password."""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)
        assert hashed != password

    def test_hash_password_returns_bcrypt_format(self):
        """Hashed password should be in bcrypt format."""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)
        assert hashed.startswith("$2b$")

    def test_verify_password_correct(self):
        """Verify returns True for correct password."""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)
        assert AuthService.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Verify returns False for incorrect password."""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)
        assert AuthService.verify_password("wrongpassword", hashed) is False

    def test_different_passwords_different_hashes(self):
        """Different passwords should produce different hashes."""
        hash1 = AuthService.hash_password("password1")
        hash2 = AuthService.hash_password("password2")
        assert hash1 != hash2

    def test_same_password_different_hashes(self):
        """Same password should produce different hashes (due to salt)."""
        password = "testpassword123"
        hash1 = AuthService.hash_password(password)
        hash2 = AuthService.hash_password(password)
        assert hash1 != hash2
        # But both should verify correctly
        assert AuthService.verify_password(password, hash1)
        assert AuthService.verify_password(password, hash2)


class TestJWTTokens:
    """Tests for JWT token functionality."""

    def test_create_access_token_returns_string(self):
        """Token creation should return a string."""
        token = AuthService.create_access_token(user_id=1)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_different_for_different_users(self):
        """Different users should get different tokens."""
        token1 = AuthService.create_access_token(user_id=1)
        token2 = AuthService.create_access_token(user_id=2)
        assert token1 != token2

    def test_decode_token_valid(self):
        """Valid token should decode successfully."""
        token = AuthService.create_access_token(user_id=42)
        payload = AuthService.decode_token(token)
        assert payload is not None
        assert payload["sub"] == "42"

    def test_decode_token_invalid(self):
        """Invalid token should return None."""
        payload = AuthService.decode_token("invalid.token.here")
        assert payload is None

    def test_decode_token_tampered(self):
        """Tampered token should return None."""
        token = AuthService.create_access_token(user_id=1)
        # Tamper with the token
        tampered = token[:-5] + "xxxxx"
        payload = AuthService.decode_token(tampered)
        assert payload is None

    def test_get_user_id_from_token_valid(self):
        """Should extract user ID from valid token."""
        token = AuthService.create_access_token(user_id=123)
        user_id = AuthService.get_user_id_from_token(token)
        assert user_id == 123

    def test_get_user_id_from_token_invalid(self):
        """Should return None for invalid token."""
        user_id = AuthService.get_user_id_from_token("invalid.token")
        assert user_id is None
