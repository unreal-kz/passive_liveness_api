from abc import ABC, abstractmethod

class ThresholdStrategy(ABC):
    """Interface for liveness evaluation strategies."""
    @abstractmethod
    def is_live(self, confidence: float, threshold: float) -> bool:
        """TODO: Implement thresholding logic."""
        pass

class FixedThresholdStrategy(ThresholdStrategy):
    """Fixed threshold strategy (stub)."""
    def is_live(self, confidence: float, threshold: float) -> bool:
        """TODO: Implement fixed threshold logic."""
        pass
