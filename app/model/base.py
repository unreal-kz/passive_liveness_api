from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np

class BaseLivenessModel(ABC):
    """
    Abstract base interface for all liveness models.
    """
    @abstractmethod
    def predict(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Predict liveness from an image.
        Args:
            image (np.ndarray): Input image array.
        Returns:
            Tuple[str, float]: (label, confidence) e.g. ("real", 0.99)
        """
        pass
