
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
import json
from pydantic import BaseModel

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
