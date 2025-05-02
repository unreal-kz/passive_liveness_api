import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.utils import get_logger
import traceback

logger = get_logger(__name__)

def register_error_handlers(app: FastAPI) -> None:
    """
    Register custom error handlers for the FastAPI app.
    Handles Exception (500) and ValueError (400) with logging.
    """
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "detail": "An unexpected error occurred."},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        logger.error(f"ValueError: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=400,
            content={"error": "Bad Request", "detail": str(exc)},
        )
