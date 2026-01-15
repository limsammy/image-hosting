"""
Pydantic schemas for user-related requests and responses.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration request."""

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Username (letters, numbers, underscore, hyphen only)",
    )
    email: EmailStr = Field(description="User's email address")
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password (minimum 8 characters)",
    )


class UserResponse(BaseModel):
    """Schema for user data in responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    created_at: datetime


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
