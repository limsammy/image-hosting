"""
Image management routes: upload, list, and delete.
"""

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import func, select

from app.dependencies import CurrentUser, SessionDep
from app.models import Image
from app.schemas import (
    ImageConfirmRequest,
    ImageListResponse,
    ImageResponse,
    ImageUploadRequest,
    ImageUploadResponse,
)
from app.services import storage

router = APIRouter(prefix="/api/images", tags=["images"])


@router.post("/upload-url", response_model=ImageUploadResponse)
async def get_upload_url(
    request: ImageUploadRequest,
    current_user: CurrentUser,
) -> dict:
    """Get a presigned URL for uploading an image directly to R2."""
    r2_key = storage.generate_key(current_user.id, request.filename)
    upload_url = storage.generate_upload_url(r2_key, request.content_type)
    public_url = storage.get_public_url(r2_key)

    return {
        "upload_url": upload_url,
        "r2_key": r2_key,
        "public_url": public_url,
    }


@router.post("/confirm", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def confirm_upload(
    request: ImageConfirmRequest,
    current_user: CurrentUser,
    session: SessionDep,
) -> Image:
    """
    Confirm an upload completed and save metadata to database.
    Verifies the file exists in R2 before saving.
    """
    # Verify the r2_key belongs to this user (security check first)
    if not request.r2_key.startswith(f"{current_user.id}/"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid storage key",
        )

    # Verify the object exists in R2
    obj_info = storage.verify_object_exists(request.r2_key)
    if obj_info is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File not found in storage. Upload may have failed.",
        )

    # Check if already confirmed (duplicate request)
    result = await session.execute(
        select(Image).where(Image.r2_key == request.r2_key)
    )
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Image already confirmed",
        )

    # Create image record
    image = Image(
        user_id=current_user.id,
        filename=request.filename,
        r2_key=request.r2_key,
        content_type=request.content_type,
        size_bytes=obj_info["size_bytes"],
        public_url=storage.get_public_url(request.r2_key),
    )
    session.add(image)
    await session.flush()
    await session.refresh(image)

    return image


@router.get("/", response_model=ImageListResponse)
async def list_images(
    current_user: CurrentUser,
    session: SessionDep,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
) -> dict:
    """List all images for the current user with pagination."""
    offset = (page - 1) * per_page

    # Get total count
    count_result = await session.execute(
        select(func.count(Image.id)).where(Image.user_id == current_user.id)
    )
    total = count_result.scalar() or 0

    # Get images for this page
    result = await session.execute(
        select(Image)
        .where(Image.user_id == current_user.id)
        .order_by(Image.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    images = result.scalars().all()

    return {
        "images": images,
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/{image_id}", response_model=ImageResponse)
async def get_image(
    image_id: int,
    current_user: CurrentUser,
    session: SessionDep,
) -> Image:
    """Get a single image by ID."""
    result = await session.execute(
        select(Image).where(Image.id == image_id, Image.user_id == current_user.id)
    )
    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )

    return image


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: int,
    current_user: CurrentUser,
    session: SessionDep,
) -> None:
    """Delete an image from R2 and database."""
    result = await session.execute(
        select(Image).where(Image.id == image_id, Image.user_id == current_user.id)
    )
    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )

    # Delete from R2 first
    storage.delete_object(image.r2_key)

    # Then delete from database
    await session.delete(image)
    await session.flush()
