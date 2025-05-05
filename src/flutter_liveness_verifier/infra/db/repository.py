import time
from sqlalchemy.exc import SQLAlchemyError
from .session import SessionLocal
from .models import LivenessVerdict
import uuid

def save_liveness_verdict(payload: dict) -> str:
    session = SessionLocal()
    try:
        verdict = LivenessVerdict(
            id=uuid.uuid4(),
            user_id=payload["user_id"],
            device_id=payload["device_id"],
            score=payload["liveness_score"],
            verdict=payload["verdict"],
            ts=payload["timestamp"],
            session_id=payload["session_id"]
        )
        session.add(verdict)
        session.commit()
        return str(verdict.id)
    except SQLAlchemyError as e:
        session.rollback()
        # Retry once after a short delay
        time.sleep(1)
        try:
            session.add(verdict)
            session.commit()
            return str(verdict.id)
        except Exception as e2:
            session.rollback()
            raise e2
    finally:
        session.close()
