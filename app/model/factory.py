from .base import BaseLivenessModel
from .onnx_model import OnnxLivenessModel
from .pytorch_model import PytorchLivenessModel
from passive_liveness_api.app.utils import get_logger

logger = get_logger(__name__)

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
        logger.info(f"Loading model type '{t}' from path '{model_path}'")
        if t == "onnx":
            logger.info("ONNX model loaded.")
            return OnnxLivenessModel(model_path)
        elif t == "pytorch":
            logger.info("PyTorch model loaded.")
            return PytorchLivenessModel(model_path)
        else:
            logger.error(f"Unknown model_type: {model_type}")
            raise ValueError(f"Unknown model_type: {model_type}")
