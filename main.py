from fastapi import FastAPI
from passive_liveness_api.app.handlers import router
from passive_liveness_api.app.handlers.error_handlers import register_error_handlers
from passive_liveness_api.app.utils import get_logger

app = FastAPI(title="Passive Liveness API")

# Set up root logger at INFO level
logger = get_logger()
logger.info("Starting Passive Liveness API service.")

# Register error handlers
register_error_handlers(app)

app.include_router(router)
