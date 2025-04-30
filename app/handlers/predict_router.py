from fastapi import APIRouter

router = APIRouter()

@router.post("/liveness")
def predict_liveness():
    """Stub endpoint for liveness prediction."""
    # TODO: implement endpoint logic
    return {"detail": "Not Implemented"}
