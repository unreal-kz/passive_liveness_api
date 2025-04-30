from fastapi import APIRouter, Depends, Security
from .schemas import LivenessRequest, LivenessResponse
from passive_liveness_api.app.utils import get_logger
from passive_liveness_api.app.handlers.security import check_api_key

router = APIRouter()
logger = get_logger(__name__)

def get_pipeline():
    """
    Dependency provider for the inference pipeline.
    TODO: Return a real InferencePipeline instance.
    """
    # TODO: Replace with actual pipeline instantiation
    return None

from passive_liveness_api.app.utils.async_exec import run_in_thread

@router.post(
    "/liveness",
    response_model=LivenessResponse,
    summary="Passive liveness check",
    description="""
    Accepts a base64-encoded face image and returns a liveness decision.\n\n
    **Authentication:**
    - Supply either `X-API-KEY` header or `Authorization: Bearer <token>` header.\n
    Returns liveness label, confidence, and active check fallback if needed.
    """,
    tags=["Liveness"],
)
async def liveness_endpoint(
    request: LivenessRequest,
    pipeline=Depends(get_pipeline),
    api_key=Depends(check_api_key),
):
    """
    Accepts a base64 face image, calls the inference pipeline, and returns a response.
    Offloads inference to a thread-pool for async responsiveness.
    """
    logger.info("/liveness request received.")
    # TODO: Replace with: result = await run_in_thread(pipeline.run, image)
    dummy_result = {
        "liveness_label": "real",
        "confidence_score": 0.99,
        "requires_active_check": False,
    }
    logger.info(f"/liveness response: {dummy_result}")
    return LivenessResponse(**dummy_result)
