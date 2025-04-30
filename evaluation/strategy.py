from abc import ABC, abstractmethod

class EvaluationStrategy(ABC):
    @abstractmethod
    def evaluate(self, confidence: float, threshold: float) -> dict:
        """Returns dict with liveness_label, requires_active_check."""
        pass

class ThresholdStrategy(EvaluationStrategy):
    def evaluate(self, confidence: float, threshold: float) -> dict:
        if confidence >= threshold:
            return {"liveness_label": "real", "requires_active_check": False}
        else:
            return {"liveness_label": "fake", "requires_active_check": True}
