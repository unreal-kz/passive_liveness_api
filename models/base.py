from abc import ABC, abstractmethod
import numpy as np

class LivenessModel(ABC):
    @abstractmethod
    def predict(self, image: np.ndarray) -> float:
        """Returns confidence score (0.0–1.0) for liveness."""
        pass
