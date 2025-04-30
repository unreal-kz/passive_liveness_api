import httpx
import pytest
from fastapi import status
from passive_liveness_api.main import app

@pytest.mark.asyncio
async def test_metrics_endpoint_enabled(monkeypatch):
    monkeypatch.setenv('ENABLE_METRICS', 'true')
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.get("/metrics")
        assert resp.status_code == status.HTTP_200_OK
        assert b'liveness_requests_total' in resp.content

@pytest.mark.asyncio
async def test_metrics_endpoint_disabled(monkeypatch):
    monkeypatch.setenv('ENABLE_METRICS', 'false')
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.get("/metrics")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert b'Metrics disabled' in resp.content
