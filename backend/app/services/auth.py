"""
Authentication service for password hashing and JWT tokens.
"""

from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext

from app.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Handles password hashing and JWT token operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user_id: int) -> str:
        """Create a JWT access token for a user."""
        expire = datetime.now(tz=timezone.utc) + timedelta(
            minutes=settings.jwt_expiration_minutes
        )
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.now(tz=timezone.utc),
        }
        return jwt.encode(
            payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )

    @staticmethod
    def decode_token(token: str) -> dict | None:
        """
        Decode and verify a JWT token.
        Returns the payload if valid, None if invalid or expired.
        """
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
            return payload
        except ExpiredSignatureError:
            return None
        except InvalidTokenError:
            return None

    @staticmethod
    def get_user_id_from_token(token: str) -> int | None:
        """Extract user ID from a valid token."""
        payload = AuthService.decode_token(token)
        if payload is None:
            return None
        try:
            return int(payload["sub"])
        except (KeyError, ValueError):
            return None
