from fastapi import APIRouter, UploadFile, File, Request
from passive_liveness_api.app.active.blink_challenge import BlinkChallenge
from passive_liveness_api.app.utils import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/active/blink", summary="Active blink challenge", tags=["Liveness"])
async def active_blink_challenge(request: Request, video: UploadFile = File(...)):
    """
    Accepts a short video and returns whether the active blink challenge is passed.
    """
    logger.info("/active/blink challenge POST received.")
    challenge = BlinkChallenge()
    # Wrap request to inject UploadFile as files dict
    class DummyReq:
        files = {"video": video}
    result = await challenge.run(DummyReq())
    logger.info(f"/active/blink response: {result}")
    return result
