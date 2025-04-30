from abc import ABC, abstractmethod

class FallbackHandler(ABC):
    """Interface for fallback to active liveness check."""
    @abstractmethod
    def trigger(self, reason: str = "") -> None:
        """TODO: Implement fallback trigger."""
        pass

class MockFallbackHandler(FallbackHandler):
    """Mock fallback handler (stub)."""
    def trigger(self, reason: str = "") -> None:
        """TODO: Mock fallback trigger."""
        pass
