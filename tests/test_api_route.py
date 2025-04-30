import base64
from passive_liveness_api.app.handlers.schemas import LivenessResponse

def test_liveness_route(client):
    # Use a tiny placeholder image (1x1 PNG) base64 string
    image_b64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII="
    )
    payload = {"image": image_b64}
    response = client.post("/liveness", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "liveness_label" in data
    assert "confidence_score" in data
    assert "requires_active_check" in data
    # fallback_response may or may not be present (depends on stub)
