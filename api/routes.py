from fastapi import APIRouter
from passive_liveness_api.api.schemas import LivenessRequest, LivenessResponse

router = APIRouter()

@router.post("/liveness", response_model=LivenessResponse)
def check_liveness(payload: LivenessRequest):
    """Endpoint for passive liveness detection."""
    # Model loading, inference, and evaluation logic will be injected here
    # Placeholder response
    return LivenessResponse(liveness_label="real", confidence_score=1.0, requires_active_check=False)
