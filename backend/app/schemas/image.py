"""
Pydantic schemas for image-related requests and responses.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ImageUploadRequest(BaseModel):
    """Request schema for getting a presigned upload URL."""

    filename: str = Field(
        min_length=1,
        max_length=255,
        description="Original filename",
    )
    content_type: str = Field(
        pattern=r"^image/(jpeg|png|gif|webp)$",
        description="MIME type (image/jpeg, image/png, image/gif, image/webp)",
    )
    size_bytes: int = Field(
        gt=0,
        le=10_485_760,  # Max 10MB
        description="File size in bytes (max 10MB)",
    )


class ImageUploadResponse(BaseModel):
    """Response schema with presigned URL for upload."""

    upload_url: str = Field(description="Presigned R2 URL for PUT upload")
    r2_key: str = Field(description="Key/path in R2 bucket")
    public_url: str = Field(description="Public URL after upload completes")


class ImageConfirmRequest(BaseModel):
    """Request schema to confirm upload completion."""

    r2_key: str = Field(description="R2 key returned from upload-url endpoint")
    filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(pattern=r"^image/(jpeg|png|gif|webp)$")
    size_bytes: int = Field(gt=0, le=10_485_760)


class ImageResponse(BaseModel):
    """Schema for image data in responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    public_url: str
    content_type: str
    size_bytes: int
    created_at: datetime


class ImageListResponse(BaseModel):
    """Schema for paginated list of images."""

    images: list[ImageResponse]
    total: int
    page: int = 1
    per_page: int = 20
