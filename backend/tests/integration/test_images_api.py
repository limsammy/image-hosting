"""
Integration tests for images API endpoints.
"""

import os
from unittest.mock import MagicMock, patch

import boto3
import pytest
from httpx import AsyncClient
from moto import mock_aws


@pytest.fixture(scope="function")
def aws_credentials():
    """Set mocked AWS credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def mock_storage(aws_credentials, monkeypatch):
    """Mock the storage service with moto S3."""
    monkeypatch.setattr("app.config.settings.r2_bucket_name", "test-bucket")
    monkeypatch.setattr("app.config.settings.r2_public_url", "https://pub.r2.dev")
    monkeypatch.setattr("app.config.settings.r2_account_id", "test-account")
    monkeypatch.setattr("app.config.settings.r2_access_key_id", "testing")
    monkeypatch.setattr("app.config.settings.r2_secret_access_key", "testing")

    with mock_aws():
        conn = boto3.client("s3", region_name="us-east-1")
        conn.create_bucket(Bucket="test-bucket")

        # Inject mocked client into storage service
        from app.services import storage
        storage._client = conn

        yield conn


@pytest.fixture
async def auth_token(client: AsyncClient) -> str:
    """Create a user and return their auth token."""
    await client.post(
        "/api/auth/register",
        json={
            "username": "imageuser",
            "email": "imageuser@example.com",
            "password": "password123",
        },
    )
    response = await client.post(
        "/api/auth/login",
        data={"username": "imageuser", "password": "password123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    """Return authorization headers."""
    return {"Authorization": f"Bearer {auth_token}"}


class TestGetUploadUrl:
    """Tests for POST /api/images/upload-url endpoint."""

    async def test_get_upload_url_success(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should return presigned URL, r2_key, and public_url."""
        response = await client.post(
            "/api/images/upload-url",
            json={
                "filename": "test.jpg",
                "content_type": "image/jpeg",
                "size_bytes": 1024,
            },
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "upload_url" in data
        assert "r2_key" in data
        assert "public_url" in data
        assert data["r2_key"].endswith(".jpg")
        assert data["public_url"].startswith("https://pub.r2.dev/")

    async def test_get_upload_url_invalid_content_type(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should reject non-image content types."""
        response = await client.post(
            "/api/images/upload-url",
            json={
                "filename": "test.txt",
                "content_type": "text/plain",
                "size_bytes": 1024,
            },
            headers=auth_headers,
        )

        assert response.status_code == 422

    async def test_get_upload_url_file_too_large(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should reject files over 10MB."""
        response = await client.post(
            "/api/images/upload-url",
            json={
                "filename": "huge.jpg",
                "content_type": "image/jpeg",
                "size_bytes": 11_000_000,  # Over 10MB
            },
            headers=auth_headers,
        )

        assert response.status_code == 422

    async def test_get_upload_url_unauthenticated(
        self, client: AsyncClient, mock_storage
    ):
        """Should require authentication."""
        response = await client.post(
            "/api/images/upload-url",
            json={
                "filename": "test.jpg",
                "content_type": "image/jpeg",
                "size_bytes": 1024,
            },
        )

        assert response.status_code == 401


class TestConfirmUpload:
    """Tests for POST /api/images/confirm endpoint."""

    async def test_confirm_upload_success(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should save image metadata after confirming upload."""
        # First get upload URL
        url_response = await client.post(
            "/api/images/upload-url",
            json={
                "filename": "confirmed.png",
                "content_type": "image/png",
                "size_bytes": 2048,
            },
            headers=auth_headers,
        )
        r2_key = url_response.json()["r2_key"]

        # Simulate upload to R2 (mock)
        mock_storage.put_object(
            Bucket="test-bucket",
            Key=r2_key,
            Body=b"x" * 2048,
            ContentType="image/png",
        )

        # Confirm upload
        response = await client.post(
            "/api/images/confirm",
            json={
                "r2_key": r2_key,
                "filename": "confirmed.png",
                "content_type": "image/png",
                "size_bytes": 2048,
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["filename"] == "confirmed.png"
        assert data["content_type"] == "image/png"
        assert data["size_bytes"] == 2048
        assert "id" in data
        assert "public_url" in data
        assert "created_at" in data

    async def test_confirm_upload_file_not_in_r2(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should reject if file doesn't exist in R2."""
        # Get upload URL but don't actually upload
        url_response = await client.post(
            "/api/images/upload-url",
            json={
                "filename": "missing.png",
                "content_type": "image/png",
                "size_bytes": 1024,
            },
            headers=auth_headers,
        )
        r2_key = url_response.json()["r2_key"]

        # Try to confirm without uploading
        response = await client.post(
            "/api/images/confirm",
            json={
                "r2_key": r2_key,
                "filename": "missing.png",
                "content_type": "image/png",
                "size_bytes": 1024,
            },
            headers=auth_headers,
        )

        assert response.status_code == 400
        assert "not found" in response.json()["detail"].lower()

    async def test_confirm_upload_wrong_user_key(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should reject r2_key belonging to another user."""
        response = await client.post(
            "/api/images/confirm",
            json={
                "r2_key": "999/somefile.png",  # Different user ID
                "filename": "stolen.png",
                "content_type": "image/png",
                "size_bytes": 1024,
            },
            headers=auth_headers,
        )

        assert response.status_code == 403

    async def test_confirm_upload_duplicate(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should reject duplicate confirmation."""
        # Get upload URL and upload
        url_response = await client.post(
            "/api/images/upload-url",
            json={
                "filename": "dup.png",
                "content_type": "image/png",
                "size_bytes": 1024,
            },
            headers=auth_headers,
        )
        r2_key = url_response.json()["r2_key"]

        mock_storage.put_object(
            Bucket="test-bucket",
            Key=r2_key,
            Body=b"x" * 1024,
            ContentType="image/png",
        )

        # Confirm once
        await client.post(
            "/api/images/confirm",
            json={
                "r2_key": r2_key,
                "filename": "dup.png",
                "content_type": "image/png",
                "size_bytes": 1024,
            },
            headers=auth_headers,
        )

        # Try to confirm again
        response = await client.post(
            "/api/images/confirm",
            json={
                "r2_key": r2_key,
                "filename": "dup.png",
                "content_type": "image/png",
                "size_bytes": 1024,
            },
            headers=auth_headers,
        )

        assert response.status_code == 409


class TestListImages:
    """Tests for GET /api/images/ endpoint."""

    async def test_list_images_empty(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should return empty list for new user."""
        response = await client.get("/api/images/", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["images"] == []
        assert data["total"] == 0

    async def test_list_images_with_data(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should return user's images."""
        # Upload and confirm an image
        url_response = await client.post(
            "/api/images/upload-url",
            json={
                "filename": "list-test.jpg",
                "content_type": "image/jpeg",
                "size_bytes": 512,
            },
            headers=auth_headers,
        )
        r2_key = url_response.json()["r2_key"]

        mock_storage.put_object(
            Bucket="test-bucket",
            Key=r2_key,
            Body=b"x" * 512,
            ContentType="image/jpeg",
        )

        await client.post(
            "/api/images/confirm",
            json={
                "r2_key": r2_key,
                "filename": "list-test.jpg",
                "content_type": "image/jpeg",
                "size_bytes": 512,
            },
            headers=auth_headers,
        )

        # List images
        response = await client.get("/api/images/", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["images"]) == 1
        assert data["images"][0]["filename"] == "list-test.jpg"

    async def test_list_images_pagination(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should support pagination."""
        response = await client.get(
            "/api/images/",
            params={"page": 1, "per_page": 5},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["per_page"] == 5


class TestGetImage:
    """Tests for GET /api/images/{image_id} endpoint."""

    async def test_get_image_success(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should return single image by ID."""
        # Create an image
        url_response = await client.post(
            "/api/images/upload-url",
            json={
                "filename": "single.gif",
                "content_type": "image/gif",
                "size_bytes": 256,
            },
            headers=auth_headers,
        )
        r2_key = url_response.json()["r2_key"]

        mock_storage.put_object(
            Bucket="test-bucket",
            Key=r2_key,
            Body=b"x" * 256,
            ContentType="image/gif",
        )

        confirm_response = await client.post(
            "/api/images/confirm",
            json={
                "r2_key": r2_key,
                "filename": "single.gif",
                "content_type": "image/gif",
                "size_bytes": 256,
            },
            headers=auth_headers,
        )
        image_id = confirm_response.json()["id"]

        # Get single image
        response = await client.get(
            f"/api/images/{image_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert response.json()["id"] == image_id
        assert response.json()["filename"] == "single.gif"

    async def test_get_image_not_found(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should return 404 for nonexistent image."""
        response = await client.get("/api/images/99999", headers=auth_headers)
        assert response.status_code == 404


class TestDeleteImage:
    """Tests for DELETE /api/images/{image_id} endpoint."""

    async def test_delete_image_success(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should delete image from R2 and database."""
        # Create an image
        url_response = await client.post(
            "/api/images/upload-url",
            json={
                "filename": "todelete.webp",
                "content_type": "image/webp",
                "size_bytes": 128,
            },
            headers=auth_headers,
        )
        r2_key = url_response.json()["r2_key"]

        mock_storage.put_object(
            Bucket="test-bucket",
            Key=r2_key,
            Body=b"x" * 128,
            ContentType="image/webp",
        )

        confirm_response = await client.post(
            "/api/images/confirm",
            json={
                "r2_key": r2_key,
                "filename": "todelete.webp",
                "content_type": "image/webp",
                "size_bytes": 128,
            },
            headers=auth_headers,
        )
        image_id = confirm_response.json()["id"]

        # Delete image
        response = await client.delete(
            f"/api/images/{image_id}",
            headers=auth_headers,
        )

        assert response.status_code == 204

        # Verify it's gone
        get_response = await client.get(
            f"/api/images/{image_id}",
            headers=auth_headers,
        )
        assert get_response.status_code == 404

    async def test_delete_image_not_found(
        self, client: AsyncClient, auth_headers: dict, mock_storage
    ):
        """Should return 404 for nonexistent image."""
        response = await client.delete("/api/images/99999", headers=auth_headers)
        assert response.status_code == 404
