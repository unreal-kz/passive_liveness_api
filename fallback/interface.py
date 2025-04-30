from abc import ABC, abstractmethod

class FallbackTrigger(ABC):
    @abstractmethod
    def trigger(self, reason: str = "") -> None:
        """Trigger fallback to active liveness check (e.g., blink, head-turn)."""
        pass

class NoOpFallback(FallbackTrigger):
    def trigger(self, reason: str = "") -> None:
        # No operation fallback (for initial stub/testing)
        pass
