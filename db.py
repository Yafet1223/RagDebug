from datetime import datetime
import os

try:
    from sqlalchemy import Column, DateTime, Integer, Text, create_engine
    from sqlalchemy.orm import declarative_base, sessionmaker
except ImportError:  # pragma: no cover - fallback for minimal setups
    Column = DateTime = Integer = Text = create_engine = None
    declarative_base = sessionmaker = None

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/rag_debug")

if create_engine is not None:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base = declarative_base()
else:
    engine = None
    SessionLocal = None
    Base = object


class DebugLog(Base):  # type: ignore[misc,valid-type]
    __tablename__ = "debug_logs"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


Log = DebugLog


def init_db():
    if engine is None:
        return False
    try:
        Base.metadata.create_all(bind=engine)
        return True
    except Exception as exc:  # pragma: no cover - depends on local DB availability
        print(f"Database init skipped: {exc}")
        return False