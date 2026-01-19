"""
Admin routes: storage stats, image management, and user management.
Requires admin privileges (is_admin=True).
"""

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import func, select

from app.dependencies import AdminUser, SessionDep
from app.models import Image, User
from app.schemas import ImageListResponse, ImageResponse, UserResponse
from app.services import storage

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
async def get_storage_stats(
    _admin_user: AdminUser,
) -> dict:
    """
    Get R2 storage usage statistics.
    Shows total size, object count, and usage against 10GB free tier.
    """
    return storage.get_storage_stats()


@router.get("/images", response_model=ImageListResponse)
async def list_all_images(
    _admin_user: AdminUser,
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
) -> dict:
    """
    List ALL images from ALL users (admin only).
    Supports pagination via skip/limit.
    """
    # Get total count
    count_result = await session.execute(select(func.count(Image.id)))
    total = count_result.scalar_one()

    # Get paginated images
    result = await session.execute(
        select(Image)
        .order_by(Image.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    images = result.scalars().all()

    return {"images": images, "total": total}


@router.get("/images/{image_id}", response_model=ImageResponse)
async def get_any_image(
    image_id: int,
    _admin_user: AdminUser,
    session: SessionDep,
) -> Image:
    """
    Get details for any image by ID (admin only).
    """
    result = await session.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )

    return image


@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_any_image(
    image_id: int,
    _admin_user: AdminUser,
    session: SessionDep,
) -> None:
    """
    Delete any image by ID (admin only).
    Deletes from R2 and database.
    """
    # Get the image
    result = await session.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )

    # Delete from R2 first
    if not storage.delete_object(image.r2_key):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete image from storage",
        )

    # Then delete from database
    await session.delete(image)
    await session.commit()


@router.get("/users", response_model=list[UserResponse])
async def list_all_users(
    _admin_user: AdminUser,
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
) -> list[User]:
    """
    List all users (admin only).
    Supports pagination via skip/limit.
    """
    result = await session.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()

    return list(users)
