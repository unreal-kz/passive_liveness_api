from pydantic import BaseModel, Field
from typing import Optional

class LivenessRequest(BaseModel):
    image_base64: str = Field(..., description="Base64-encoded RGB face image")
    model_type: Optional[str] = Field("onnx", description="Model type: 'onnx' or 'pytorch'")

class LivenessResponse(BaseModel):
    liveness_label: str = Field(..., description="'real' or 'fake'")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    requires_active_check: bool = Field(...)
