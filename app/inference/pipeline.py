from typing import Any, Dict
from passive_liveness_api.app.model.base import BaseLivenessModel
from .strategy import ThresholdStrategy

class InferencePipeline:
    """
    Pipeline for running liveness inference using a model and strategy.
    """
    def __init__(self, model: BaseLivenessModel, strategy: ThresholdStrategy) -> None:
        """
        Initialize with model and decision strategy.
        Args:
            model (BaseLivenessModel): Liveness model.
            strategy (ThresholdStrategy): Liveness decision strategy.
        """
        self.model = model
        self.strategy = strategy

    def run(self, image: Any) -> Dict[str, object]:
        """
        Run the inference pipeline: predict, then evaluate.
        Args:
            image (Any): Input image (placeholder type).
        Returns:
            dict: Liveness decision output.
        """
        label, confidence = self.model.predict(image)
        result = self.strategy.evaluate(label, confidence)
        return result
