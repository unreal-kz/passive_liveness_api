from abc import ABC, abstractmethod
from typing import Dict

class FallbackHandler(ABC):
    """
    Interface for fallback to active liveness check.
    """
    @abstractmethod
    def trigger_fallback(self, reason: str = "") -> Dict[str, str]:
        """
        Trigger a fallback and return a dictionary describing the required client action.
        Args:
            reason (str): Reason for fallback (optional).
        Returns:
            dict: Fallback response for the client.
        """
        pass

class MockFallbackHandler(FallbackHandler):
    """
    Placeholder fallback handler that returns a static message.
    """
    def trigger_fallback(self, reason: str = "") -> Dict[str, str]:
        return {"message": "Please blink or turn your head."}
