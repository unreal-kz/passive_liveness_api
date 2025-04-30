import pytest
from passive_liveness_api.app.inference.strategy import FixedThresholdStrategy
from passive_liveness_api.app.inference.pipeline import InferencePipeline
from passive_liveness_api.app.inference.fallback import MockFallbackHandler

class DummyModel:
    def __init__(self, label, confidence):
        self.label = label
        self.confidence = confidence
    def predict(self, image):
        return self.label, self.confidence

def test_pipeline_real_above_threshold():
    model = DummyModel("real", 0.99)
    strategy = FixedThresholdStrategy(0.85)
    fallback = MockFallbackHandler()
    pipeline = InferencePipeline(model, strategy, fallback)
    result = pipeline.run("dummy_image")
    assert result["liveness_label"] == "real"
    assert result["confidence_score"] == 0.99
    assert result["requires_active_check"] is False
    assert "fallback_response" not in result

def test_pipeline_fake_below_threshold():
    model = DummyModel("fake", 0.7)
    strategy = FixedThresholdStrategy(0.85)
    fallback = MockFallbackHandler()
    pipeline = InferencePipeline(model, strategy, fallback)
    result = pipeline.run("dummy_image")
    assert result["liveness_label"] == "fake"
    assert result["confidence_score"] == 0.7
    assert result["requires_active_check"] is True
    assert "fallback_response" in result
    assert "message" in result["fallback_response"]
