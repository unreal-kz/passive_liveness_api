from passive_liveness_api.models.base import LivenessModel
import numpy as np

class OnnxLivenessModel(LivenessModel):
    def __init__(self, model_path: str):
        # Placeholder for ONNX model loading
        self.model_path = model_path
        self.model = None  # Load ONNX model here

    def predict(self, image: np.ndarray) -> float:
        # Placeholder for ONNX model inference
        return 1.0
