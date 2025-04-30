from abc import ABC, abstractmethod

class BaseLivenessModel(ABC):
    """Interface for liveness models."""
    @abstractmethod
    def predict(self, image):
        """Run liveness prediction. TODO: define input/output."""
        pass  # TODO: implement in subclass
