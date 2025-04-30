import pytest
from passive_liveness_api.app.model.factory import LivenessModelFactory
from passive_liveness_api.app.model.onnx_model import OnnxLivenessModel
from passive_liveness_api.app.model.pytorch_model import PytorchLivenessModel

def test_factory_loads_onnx():
    model = LivenessModelFactory.load("onnx", "dummy/path")
    assert isinstance(model, OnnxLivenessModel)

def test_factory_loads_pytorch():
    model = LivenessModelFactory.load("pytorch", "dummy/path")
    assert isinstance(model, PytorchLivenessModel)

@pytest.mark.parametrize("bad_type", ["tf", "", None])
def test_factory_raises_on_unknown_type(bad_type):
    with pytest.raises(ValueError):
        LivenessModelFactory.load(bad_type, "dummy/path")
