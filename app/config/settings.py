"""Global settings and constants (TODO)."""
import os
from functools import lru_cache
try:
    from multiprocessing import cpu_count
except ImportError:
    def cpu_count():
        return 4

class Settings:
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/silentface.onnx")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", 0.85))
    ENABLE_FALLBACK: bool = os.getenv("ENABLE_FALLBACK", "true").lower() == "true"
    API_KEY: str = os.getenv("API_KEY", None)
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", cpu_count()))
