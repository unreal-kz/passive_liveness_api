
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import json
from pydantic import BaseModel

from src.flutter_liveness_verifier.adapters.http.schema import LivenessVerdictIngestRequest, LivenessVerdictIngestResponse
from src.flutter_liveness_verifier.infra.db import save_liveness_verdict
from src.flutter_liveness_verifier.adapters.kafka_producer import publish_liveness_verified

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthResponse(BaseModel):
    status: str = "ok"

app = FastAPI()

# Enable CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health():
    logger.info("Health endpoint called")
    return HealthResponse()


@app.post("/api/v1/liveness-verdict", response_model=LivenessVerdictIngestResponse, status_code=status.HTTP_202_ACCEPTED)
async def ingest_liveness_verdict(payload: LivenessVerdictIngestRequest):
    logger.info(f"Received verdict: {payload.dict()}")
    # Save to DB
    message_id = save_liveness_verdict(payload.dict())
    # Publish to Kafka
    publish_liveness_verified(payload.dict())
    return LivenessVerdictIngestResponse(message_id=message_id)
