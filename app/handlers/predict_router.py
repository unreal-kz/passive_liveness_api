from fastapi import APIRouter, Depends
from .schemas import LivenessRequest, LivenessResponse

router = APIRouter()

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
    # TODO: Replace with: result = pipeline.run(image)
    dummy_result = {
        "liveness_label": "real",
        "confidence_score": 0.99,
        "requires_active_check": False,
    }
    return LivenessResponse(**dummy_result)
