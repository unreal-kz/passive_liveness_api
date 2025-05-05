import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/liveness_db")

def get_engine():
    return create_engine(DB_URL, pool_pre_ping=True, pool_recycle=3600, poolclass=NullPool, connect_args={"connect_timeout": 5})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
