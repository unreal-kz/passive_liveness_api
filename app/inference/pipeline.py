from typing import Any, Dict, Optional
from passive_liveness_api.app.model.base import BaseLivenessModel
from .strategy import ThresholdStrategy
from .fallback import FallbackHandler
from passive_liveness_api.app.utils import get_logger

logger = get_logger(__name__)

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
        logger.info("Inference started.")
        label, confidence = self.model.predict(image)
        logger.info(f"Model prediction: label={label}, confidence={confidence}")
        result = self.strategy.evaluate(label, confidence)
        logger.info(f"Strategy evaluation result: {result}")
        if result.get("requires_active_check"):
            logger.info("requires_active_check=True")
            if self.fallback_handler:
                fallback = self.fallback_handler.trigger_fallback(
                    reason="Passive check inconclusive"
                )
                logger.info(f"Fallback triggered: {fallback}")
                result["fallback_response"] = fallback
        logger.info("Inference finished.")
        return result
