"""
Unit tests for R2 storage service using moto to mock S3-compatible API.
"""

import os

import boto3
import pytest
from moto import mock_aws

from app.services.storage import R2Storage


@pytest.fixture(scope="function")
def aws_credentials():
    """Set mocked AWS credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def mock_s3(aws_credentials):
    """Create a mocked S3 environment with a test bucket."""
    with mock_aws():
        conn = boto3.client("s3", region_name="us-east-1")
        conn.create_bucket(Bucket="test-bucket")
        yield conn


@pytest.fixture
def storage(mock_s3, monkeypatch):
    """Create R2Storage instance configured to use mocked S3."""
    monkeypatch.setattr("app.config.settings.r2_bucket_name", "test-bucket")
    monkeypatch.setattr("app.config.settings.r2_public_url", "https://pub.r2.dev")
    monkeypatch.setattr("app.config.settings.r2_account_id", "test-account")
    monkeypatch.setattr("app.config.settings.r2_access_key_id", "testing")
    monkeypatch.setattr("app.config.settings.r2_secret_access_key", "testing")

    storage = R2Storage()
    # Override the client with our mocked one
    storage._client = mock_s3
    return storage


class TestGenerateKey:
    """Tests for key generation."""

    def test_generate_key_includes_user_id(self, storage):
        """Generated key should start with user_id."""
        key = storage.generate_key(123, "photo.jpg")
        assert key.startswith("123/")

    def test_generate_key_preserves_extension(self, storage):
        """Generated key should preserve file extension."""
        assert storage.generate_key(1, "photo.jpg").endswith(".jpg")
        assert storage.generate_key(1, "image.PNG").endswith(".png")
        assert storage.generate_key(1, "animated.gif").endswith(".gif")
        assert storage.generate_key(1, "modern.webp").endswith(".webp")

    def test_generate_key_handles_no_extension(self, storage):
        """Generated key should default to .bin for files without extension."""
        key = storage.generate_key(1, "noextension")
        assert key.endswith(".bin")

    def test_generate_key_unique(self, storage):
        """Each generated key should be unique."""
        keys = [storage.generate_key(1, "photo.jpg") for _ in range(100)]
        assert len(set(keys)) == 100


class TestPublicUrl:
    """Tests for public URL generation."""

    def test_get_public_url(self, storage):
        """Public URL should combine base URL and key."""
        url = storage.get_public_url("123/abc.jpg")
        assert url == "https://pub.r2.dev/123/abc.jpg"


class TestUploadUrl:
    """Tests for presigned upload URL generation."""

    def test_generate_upload_url_returns_string(self, storage):
        """Should return a presigned URL string."""
        url = storage.generate_upload_url("123/abc.jpg", "image/jpeg")
        assert isinstance(url, str)
        assert "123/abc.jpg" in url or "test-bucket" in url


class TestVerifyObject:
    """Tests for object verification."""

    def test_verify_object_exists_found(self, storage, mock_s3):
        """Should return object info when object exists."""
        # Upload a test object
        mock_s3.put_object(
            Bucket="test-bucket",
            Key="123/test.png",
            Body=b"fake image data",
            ContentType="image/png",
        )

        result = storage.verify_object_exists("123/test.png")

        assert result is not None
        assert result["size_bytes"] == 15  # len(b"fake image data")
        assert result["content_type"] == "image/png"

    def test_verify_object_exists_not_found(self, storage):
        """Should return None when object doesn't exist."""
        result = storage.verify_object_exists("123/missing.png")
        assert result is None


class TestDeleteObject:
    """Tests for object deletion."""

    def test_delete_object_success(self, storage, mock_s3):
        """Should return True on successful delete."""
        # Upload a test object first
        mock_s3.put_object(
            Bucket="test-bucket",
            Key="123/to-delete.png",
            Body=b"data",
            ContentType="image/png",
        )

        result = storage.delete_object("123/to-delete.png")

        assert result is True
        # Verify it's actually deleted
        assert storage.verify_object_exists("123/to-delete.png") is None

    def test_delete_object_nonexistent(self, storage):
        """Should return True even for nonexistent objects (S3 behavior)."""
        result = storage.delete_object("123/never-existed.png")
        # S3 delete is idempotent - doesn't error on missing objects
        assert result is True
