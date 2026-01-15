"""
Image ORM model for storing image metadata.
Actual image files are stored in Cloudflare R2.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Image(Base):
    """Image metadata stored in database. Actual files in R2."""

    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    r2_key: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )
    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    public_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        nullable=False,
    )

    # Relationship to user
    user: Mapped["User"] = relationship(back_populates="images")

    def __repr__(self) -> str:
        return f"<Image(id={self.id}, filename={self.filename!r})>"
