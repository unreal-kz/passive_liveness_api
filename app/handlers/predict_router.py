from fastapi import APIRouter, Depends
from .schemas import LivenessRequest, LivenessResponse
from passive_liveness_api.app.utils import get_logger

router = APIRouter()
logger = get_logger(__name__)

def get_pipeline():
    """
    Dependency provider for the inference pipeline.
    TODO: Return a real InferencePipeline instance.
    """
    # TODO: Replace with actual pipeline instantiation
    return None

@router.post("/liveness", response_model=LivenessResponse)
def liveness_endpoint(request: LivenessRequest, pipeline=Depends(get_pipeline)):
    """
    Accepts a base64 face image, calls the inference pipeline, and returns a response.
    Currently returns a placeholder response.
    """
    logger.info("/liveness request received.")
    # TODO: Replace with: result = pipeline.run(image)
    dummy_result = {
        "liveness_label": "real",
        "confidence_score": 0.99,
        "requires_active_check": False,
    }
    logger.info(f"/liveness response: {dummy_result}")
    return LivenessResponse(**dummy_result)
