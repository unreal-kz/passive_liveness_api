from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class LivenessVerdict(Base):
    __tablename__ = "liveness_verdicts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(String, nullable=False)
    device_id = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    verdict = Column(String, nullable=False)
    ts = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    session_id = Column(String, nullable=False)
