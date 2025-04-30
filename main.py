from fastapi import FastAPI
from passive_liveness_api.app.handlers import router
from passive_liveness_api.app.handlers.error_handlers import register_error_handlers
from passive_liveness_api.app.utils import get_logger

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
