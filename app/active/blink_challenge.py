from typing import Any, Dict
from .interface import ActiveChallenge
from .blink_detector import BlinkDetector

class BlinkChallenge(ActiveChallenge):
    """
    Implements the blink-detection active liveness challenge.
    Accepts a short video (3-5s) and returns {"active_passed": bool}.
    """
    def __init__(self):
        self.detector = BlinkDetector()

    async def run(self, request: Any) -> Dict:
        # Expects: request.files["video"] (starlette Request or FastAPI UploadFile)
        video_bytes = await request.files["video"].read() if hasattr(request.files["video"], "read") else await request.files["video"][0].read()
        result = self.detector.detect(video_bytes)
        return {"active_passed": bool(result)}
