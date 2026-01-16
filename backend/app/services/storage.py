"""
R2 storage service for generating presigned URLs and managing objects.
Uses boto3 with S3-compatible API for Cloudflare R2.
"""

import uuid
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from app.config import settings


class R2Storage:
    """Handles R2 object storage operations via S3-compatible API."""

    def __init__(self) -> None:
        """Initialize R2 storage. Client is created lazily on first use."""
        self._client = None

    @property
    def bucket(self) -> str:
        """Get the bucket name from settings."""
        return settings.r2_bucket_name

    @property
    def public_url(self) -> str:
        """Get the public URL base from settings."""
        return settings.r2_public_url.rstrip("/")

    @property
    def client(self):
        """Lazily create the boto3 S3 client on first access."""
        if self._client is None:
            if not settings.r2_account_id:
                raise RuntimeError("R2_ACCOUNT_ID not configured")
            self._client = boto3.client(
                "s3",
                endpoint_url=f"https://{settings.r2_account_id}.r2.cloudflarestorage.com",
                aws_access_key_id=settings.r2_access_key_id,
                aws_secret_access_key=settings.r2_secret_access_key,
                config=Config(signature_version="s3v4"),
            )
        return self._client

    def generate_key(self, user_id: int, filename: str) -> str:
        """Generate a unique R2 key for an upload."""
        ext = Path(filename).suffix.lower() or ".bin"
        unique_id = uuid.uuid4().hex
        return f"{user_id}/{unique_id}{ext}"

    def get_public_url(self, key: str) -> str:
        """Get the public URL for an object."""
        return f"{self.public_url}/{key}"

    def generate_upload_url(
        self, key: str, content_type: str, expires_in: int = 3600
    ) -> str:
        """Generate a presigned PUT URL for direct upload to R2."""
        return self.client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )

    def verify_object_exists(self, key: str) -> dict | None:
        """
        Verify an object exists in R2 after upload.
        Returns object metadata if exists, None otherwise.
        """
        try:
            response = self.client.head_object(Bucket=self.bucket, Key=key)
            return {
                "size_bytes": response["ContentLength"],
                "content_type": response["ContentType"],
            }
        except ClientError:
            return None

    def delete_object(self, key: str) -> bool:
        """Delete an object from R2. Returns True on success."""
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False


# Global storage instance
storage = R2Storage()
