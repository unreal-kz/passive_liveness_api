from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LivenessVerdictIngestRequest(BaseModel):
    user_id: str = Field(...)
    timestamp: datetime = Field(...)
    device_id: str = Field(...)
    liveness_score: float = Field(...)
    verdict: str = Field(...)
    session_id: str = Field(...)

class LivenessVerdictIngestResponse(BaseModel):
    message_id: str
    status: str = "accepted"
