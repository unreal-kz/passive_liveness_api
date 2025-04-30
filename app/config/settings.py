"""Global settings and constants (TODO)."""
import os

THRESHOLD = 0.85  # TODO: Make configurable
MODEL_PATH = "path/to/model"  # TODO: Set actual model path
ENABLE_FALLBACK = True  # Toggle fallback behaviour for active liveness
API_KEY = os.getenv("API_KEY", None)
