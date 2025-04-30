from .base import BaseLivenessModel
from .onnx_model import OnnxLivenessModel
from .pytorch_model import PytorchLivenessModel

class LivenessModelFactory:
    """
    Factory for loading liveness models by type.
    """
    @staticmethod
    def load(model_type: str, model_path: str) -> BaseLivenessModel:
        """
        Load a liveness model of the given type.
        Args:
            model_type (str): 'onnx' or 'pytorch'.
            model_path (str): Path to the model file.
        Returns:
            BaseLivenessModel: Model instance.
        Raises:
            ValueError: If model_type is not supported.
        """
        t = model_type.lower()
        if t == "onnx":
            return OnnxLivenessModel(model_path)
        elif t == "pytorch":
            return PytorchLivenessModel(model_path)
        else:
            raise ValueError(f"Unknown model_type: {model_type}")
