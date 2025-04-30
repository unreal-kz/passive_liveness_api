from typing import Any, Dict, Optional
from passive_liveness_api.app.model.base import BaseLivenessModel
from .strategy import ThresholdStrategy
from .fallback import FallbackHandler

class InferencePipeline:
    """
    Pipeline for running liveness inference using a model, strategy, and optional fallback handler.
    """
    def __init__(
        self,
        model: BaseLivenessModel,
        strategy: ThresholdStrategy,
        fallback_handler: Optional[FallbackHandler] = None,
    ) -> None:
        """
        Initialize with model, decision strategy, and optional fallback handler.
        Args:
            model (BaseLivenessModel): Liveness model.
            strategy (ThresholdStrategy): Liveness decision strategy.
            fallback_handler (Optional[FallbackHandler]): Fallback handler for active checks.
        """
        self.model = model
        self.strategy = strategy
        self.fallback_handler = fallback_handler

    def run(self, image: Any) -> Dict[str, object]:
        """
        Run the inference pipeline: predict, evaluate, and optionally trigger fallback.
        Args:
            image (Any): Input image (placeholder type).
        Returns:
            dict: Liveness decision output, possibly with fallback_response.
        """
        label, confidence = self.model.predict(image)
        result = self.strategy.evaluate(label, confidence)
        if result.get("requires_active_check") and self.fallback_handler:
            fallback = self.fallback_handler.trigger_fallback(
                reason="Passive check inconclusive"
            )
            result["fallback_response"] = fallback
        return result
