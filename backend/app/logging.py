"""
Loguru logging configuration.
Configures structured logging with LOG_LEVEL from environment.
"""

import logging
import sys

from loguru import logger

from app.config import settings


class InterceptHandler(logging.Handler):
    """Intercept standard logging and redirect to Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging() -> None:
    """Configure Loguru as the main logging handler."""
    # Remove default handler
    logger.remove()

    # Add custom handler with format based on log level
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level.upper(),
        colorize=True,
    )

    # Intercept standard logging (uvicorn, sqlalchemy, etc.)
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Set specific loggers to appropriate levels
    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logging.getLogger(logger_name).handlers = [InterceptHandler()]

    # Reduce SQLAlchemy noise unless in DEBUG
    if settings.log_level.upper() != "DEBUG":
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
