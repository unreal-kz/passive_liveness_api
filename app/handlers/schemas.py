from pydantic import BaseModel, Field
from typing import Literal

class LivenessRequest(BaseModel):
    """
    Request model for liveness detection. Contains a base64-encoded RGB face image.
    """
    image_base64: str = Field(..., description="Base64-encoded RGB face image")

class LivenessResponse(BaseModel):
    """
    Response model for liveness detection.
    """
    liveness_label: Literal["real", "fake"] = Field(..., description="Liveness result label")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0-1.0)")
    requires_active_check: bool = Field(..., description="Whether active check is required")
