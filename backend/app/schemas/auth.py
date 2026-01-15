"""
Pydantic schemas for authentication requests and responses.
"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Schema for login request."""

    username: str = Field(description="Username or email")
    password: str = Field(description="User password")


class TokenResponse(BaseModel):
    """Schema for JWT token response."""

    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenPayload(BaseModel):
    """Schema for decoded JWT token payload."""

    sub: str = Field(description="Subject (user ID)")
    exp: int = Field(description="Expiration timestamp")
