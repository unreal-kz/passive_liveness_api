from typing import Tuple
import numpy as np
from .base import BaseLivenessModel

class OnnxLivenessModel(BaseLivenessModel):
    """
    ONNX-based implementation of BaseLivenessModel (placeholder).
    """
    def __init__(self, model_path: str) -> None:
        """
        Store ONNX model path. Try importing onnxruntime if available.
        """
        self.model_path = model_path
        try:
            import onnxruntime  # noqa: F401
        except ImportError:
            pass  # OK if not installed for now

    def predict(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Placeholder prediction for ONNX model.
        """
        return ("real", 0.99)
