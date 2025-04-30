from abc import ABC, abstractmethod
from typing import Any, Dict

class ActiveChallenge(ABC):
    @abstractmethod
    async def run(self, request: Any) -> Dict:
        """
        Run the active liveness challenge. Returns a result JSON fragment.
        """
        pass
