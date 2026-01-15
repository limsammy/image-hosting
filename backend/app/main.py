"""
FastAPI application with CORS, logging, and route configuration.
"""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.logging import setup_logging
from app.routers import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: setup logging on startup."""
    setup_logging()
    yield


app = FastAPI(
    title="Image Hosting API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
