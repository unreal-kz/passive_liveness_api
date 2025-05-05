import os
import hmac
import hashlib
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("API_HMAC_SECRET", "changeme")  # Should be set in .env or vault
HEADER_NAME = "x-hmac-signature"

class HMACAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Only protect specific endpoints
        if request.url.path.startswith("/api/v1/liveness-verdict"):
            signature = request.headers.get(HEADER_NAME)
            body = await request.body()
            expected = hmac.new(SECRET_KEY.encode(), body, hashlib.sha256).hexdigest()
            if not signature or not hmac.compare_digest(signature, expected):
                logger.warning(f"Auth failed: Invalid HMAC for {request.url.path}")
                raise HTTPException(status_code=401, detail="Invalid or missing HMAC signature.")
        response = await call_next(request)
        return response
