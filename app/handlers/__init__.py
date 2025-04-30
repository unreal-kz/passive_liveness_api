from .predict_router import router
from .active_router import router as active_router

# Include active challenge endpoints
router.include_router(active_router)

