from pydantic import BaseModel, Field
from typing import Literal, Optional

class LivenessRequest(BaseModel):
    """
    Request model for liveness detection. Contains a base64-encoded RGB face image.
    """
    image_base64: str = Field(..., description="Base64-encoded RGB face image")

class FallbackDescriptor(BaseModel):
    """
    Descriptor for required active challenge fallback.
    """
    challenge_type: str = Field(..., description="Type of active challenge, e.g. 'blink'")
    upload_url: str = Field(..., description="Presigned URL for uploading challenge video")

class LivenessResponse(BaseModel):
    """
    Response model for liveness detection.
    """
    liveness_label: Literal["real", "fake"] = Field(..., description="Liveness result label")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0-1.0)")
    requires_active_check: bool = Field(..., description="Whether active check is required")
    fallback: Optional[FallbackDescriptor] = Field(None, description="Active challenge fallback descriptor")
