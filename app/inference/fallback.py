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

class BlinkFallbackHandler(FallbackHandler):
    """
    Fallback handler that returns a blink challenge descriptor and upload URL.
    """
    def trigger_fallback(self, reason: str = "") -> Dict[str, str]:
        return {
            "challenge_type": "blink",
            "upload_url": "https://example.com/upload/blink123"  # Presigned URL placeholder
        }
