from fastapi import FastAPI
from app.handlers import router
from app.handlers.error_handlers import register_error_handlers
from app.utils import get_logger

app = FastAPI(
    title="Passive Liveness API",
    version="0.1.0",
    description="""
    A modular FastAPI backend for passive liveness detection in onboarding workflows.\n\n
    Receives a base64-encoded face image and returns a liveness decision, with optional fallback to active checks.
    """,
    contact={
        "name": "Your Team",
        "email": "contact@example.com",
        "url": "https://github.com/your-org/passive_liveness_api"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {"name": "Liveness", "description": "Endpoints for passive and active liveness checks."}
    ]
)

# Set up root logger at INFO level
logger = get_logger()
logger.info("Starting Passive Liveness API service.")

# Register error handlers
register_error_handlers(app)

app.include_router(router)

from contextlib import asynccontextmanager
from app.utils.async_exec import shutdown_executor
import os
from app.middleware.metrics_middleware import MetricsMiddleware
from app.middleware.tracing_middleware import TracingMiddleware

@asynccontextmanager
async def lifespan(app):
    yield
    shutdown_executor()

app.router.lifespan_context = lifespan

# --- Observability ---
from fastapi import Request, Response
from fastapi.responses import PlainTextResponse
ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
ENABLE_TRACING = os.getenv('ENABLE_TRACING', 'true').lower() == 'true'

if ENABLE_TRACING:
    app.add_middleware(TracingMiddleware)
if ENABLE_METRICS:
    app.add_middleware(MetricsMiddleware)
    try:
        from prometheus_fastapi_instrumentator import Instrumentator
        Instrumentator().instrument(app).expose(app, include_in_schema=False, endpoint="/metrics")
    except ImportError:
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
        @app.get("/metrics", include_in_schema=False)
        async def metrics():
            return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
else:
    @app.get("/metrics", include_in_schema=False)
    async def metrics_disabled():
        return PlainTextResponse("Metrics disabled", status_code=404)
