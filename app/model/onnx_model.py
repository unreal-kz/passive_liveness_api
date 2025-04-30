from typing import Tuple
import numpy as np
import os
from .base import BaseLivenessModel
from passive_liveness_api.app.utils.logger import get_logger

logger = get_logger(__name__)

class OnnxLivenessModel(BaseLivenessModel):
    """
    ONNX-based implementation of BaseLivenessModel.
    Loads and runs inference using onnxruntime.
    """
    def __init__(self, model_path: str = None) -> None:
        """
        Initialize and load ONNX model.
        Args:
            model_path (str): Path to ONNX model. Defaults to env MODEL_PATH or models/silentface.onnx.
        Raises:
            FileNotFoundError: If model file is missing.
            ImportError: If onnxruntime is not installed.
        """
        self.model_path = (
            model_path or os.getenv("MODEL_PATH") or "models/silentface.onnx"
        )
        if not os.path.isfile(self.model_path):
            raise FileNotFoundError(f"ONNX model not found at: {self.model_path}. "
                                    "Set MODEL_PATH or place model at models/silentface.onnx.")
        try:
            import onnxruntime
            self.session = onnxruntime.InferenceSession(self.model_path, providers=["CPUExecutionProvider"])
            self.input_name = self.session.get_inputs()[0].name
            self.output_name = self.session.get_outputs()[0].name
            logger.info(f"Loaded ONNX model from {self.model_path}")
        except ImportError as e:
            logger.error("onnxruntime is not installed.")
            raise ImportError("onnxruntime is required for ONNX inference.") from e
        except Exception as e:
            logger.error(f"Failed to load ONNX model: {e}")
            raise

    def predict(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Run inference and return (label, confidence) tuple.
        Args:
            image (np.ndarray): Preprocessed image (1,3,112,112 float32)
        Returns:
            Tuple[str, float]: ("real" or "fake", confidence [0,1])
        """
        try:
            ort_inputs = {self.input_name: image}
            ort_outs = self.session.run([self.output_name], ort_inputs)
            output = ort_outs[0]
            # Output shape: (1, 2) or (1, 1, 2)
            logits = output.squeeze()
            if logits.ndim == 1 and logits.shape[0] == 2:
                pass
            elif logits.ndim == 2 and logits.shape[-1] == 2:
                logits = logits[0]
            else:
                raise ValueError(f"Unexpected model output shape: {output.shape}")
            # Softmax
            exp_logits = np.exp(logits - np.max(logits))
            probs = exp_logits / np.sum(exp_logits)
            real_prob = float(probs[1])  # [0]=spoof, [1]=real (SilentFace convention)
            label = "real" if real_prob >= 0.5 else "fake"
            return label, real_prob
        except Exception as e:
            logger.error(f"ONNX inference failed: {e}")
            raise
