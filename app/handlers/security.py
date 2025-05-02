import os
from fastapi import Header, HTTPException, Security, status, Request
from fastapi.security.api_key import APIKeyHeader, APIKey
from typing import Optional
from app.config import settings

API_KEY_NAME = "X-API-KEY"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def check_api_key(
    api_key_header: Optional[str] = Security(API_KEY_HEADER),
    authorization: Optional[str] = Header(None)
) -> str:
    """
    Accepts either X-API-KEY header or Bearer token in Authorization.
    If API_KEY is set in config, require one of these to match.
    """
    valid_key = settings.API_KEY
    if not valid_key:
        return ""
    # Check X-API-KEY
    if api_key_header and api_key_header == valid_key:
        return api_key_header
    # Check Bearer token
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        if token == valid_key:
            return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key.",
        headers={"WWW-Authenticate": "Bearer"},
    )
