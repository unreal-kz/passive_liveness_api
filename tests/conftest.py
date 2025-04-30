import pytest
from fastapi.testclient import TestClient
from passive_liveness_api.app.model.factory import LivenessModelFactory
from passive_liveness_api.app.inference.strategy import FixedThresholdStrategy
from passive_liveness_api.app.inference.pipeline import InferencePipeline
from passive_liveness_api.app.inference.fallback import MockFallbackHandler
from passive_liveness_api.main import app

class DummyModel:
    def __init__(self, label="real", confidence=0.99):
        self.label = label
        self.confidence = confidence
    def predict(self, image):
        return self.label, self.confidence

@pytest.fixture
def dummy_model():
    return DummyModel()

@pytest.fixture
def fixed_strategy():
    return FixedThresholdStrategy(threshold=0.85)

@pytest.fixture
def fallback_handler():
    return MockFallbackHandler()

@pytest.fixture
def pipeline(dummy_model, fixed_strategy, fallback_handler):
    return InferencePipeline(dummy_model, fixed_strategy, fallback_handler)

@pytest.fixture
def client(monkeypatch, pipeline):
    # Patch get_pipeline dependency to use our stub pipeline
    from passive_liveness_api.app.handlers import predict_router
    def _get_pipeline():
        return pipeline
    monkeypatch.setattr(predict_router, "get_pipeline", _get_pipeline)
    return TestClient(app)
