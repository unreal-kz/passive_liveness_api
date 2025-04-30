import argparse
import base64
import sys
from pathlib import Path
from passive_liveness_api.app.model import LivenessModelFactory
from passive_liveness_api.app.inference import FixedThresholdStrategy, InferencePipeline
from passive_liveness_api.app.inference.fallback import MockFallbackHandler


def encode_image_to_base64(image_path: str) -> str:
    """
    Read an image file and return a base64-encoded string (placeholder logic).
    """
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"Error reading image file: {e}", file=sys.stderr)
        sys.exit(2)

def main():
    parser = argparse.ArgumentParser(description="Passive Liveness API Test Harness")
    parser.add_argument("--image", required=True, help="Path to image file (e.g., samples/sample1.jpg)")
    parser.add_argument("--model-type", required=True, choices=["onnx", "pytorch"], help="Model type: onnx or pytorch")
    args = parser.parse_args()

    # Step 1: Base64 encode the image (placeholder logic)
    image_base64 = encode_image_to_base64(args.image)

    # Step 2: Instantiate pipeline components
    try:
        model = LivenessModelFactory.load(args.model_type, "dummy/path")
        strategy = FixedThresholdStrategy(threshold=0.85)
        fallback = MockFallbackHandler()
        pipeline = InferencePipeline(model, strategy, fallback_handler=fallback)
    except Exception as e:
        print(f"Error initializing pipeline: {e}", file=sys.stderr)
        sys.exit(3)

    # Step 3: Run pipeline (pass base64 string as placeholder for image)
    try:
        result = pipeline.run(image_base64)
        print(result)
        sys.exit(0)
    except Exception as e:
        print(f"Pipeline error: {e}", file=sys.stderr)
        sys.exit(4)

if __name__ == "__main__":
    main()
