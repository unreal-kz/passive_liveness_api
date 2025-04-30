from abc import ABC, abstractmethod
from typing import Dict

class ThresholdStrategy(ABC):
    """
    Abstract interface for liveness decision strategies.
    """
    @abstractmethod
    def evaluate(self, label: str, confidence: float) -> Dict[str, object]:
        """
        Decide on liveness and active check requirement.
        Args:
            label (str): Liveness label (e.g., "real", "fake").
            confidence (float): Confidence score [0.0, 1.0].
        Returns:
            dict: {liveness_label, confidence_score, requires_active_check}
        """
        pass

class FixedThresholdStrategy(ThresholdStrategy):
    """
    Fixed threshold implementation of ThresholdStrategy.
    """
    def __init__(self, threshold: float = 0.85) -> None:
        """Initialize with confidence threshold."""
        self.threshold = threshold

    def evaluate(self, label: str, confidence: float) -> Dict[str, object]:
        """
        Evaluate liveness and decide if active check is needed.
        """
        requires_active = confidence < self.threshold
        return {
            "liveness_label": label,
            "confidence_score": confidence,
            "requires_active_check": requires_active,
        }
