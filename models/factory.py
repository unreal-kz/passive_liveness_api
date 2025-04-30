from passive_liveness_api.models.base import LivenessModel
from typing import Type

class ModelFactory:
    @staticmethod
    def get_model(model_type: str) -> LivenessModel:
        # Placeholder: add ONNX/PyTorch model adapters here
        raise NotImplementedError("Model loading not implemented yet.")
