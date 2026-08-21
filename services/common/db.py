import os
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError, IntegrityError
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://skillforge:skillforge@postgres:5432/skillforge")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(max_retries: int = 10, delay_seconds: float = 1.5) -> None:
    """
    Creates all tables/enums. Safe to call from every service on startup even
    though several services boot at the same moment against a shared, possibly
    not-yet-ready database:
      - retries while Postgres is still starting (OperationalError)
      - tolerates a concurrent CREATE TYPE/CREATE TABLE race from a sibling
        service (ProgrammingError/IntegrityError "already exists") by retrying
        once more, since the second attempt will see the object already there
        and skip it via checkfirst.
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError as e:
            last_error = e
            time.sleep(delay_seconds)
        except (ProgrammingError, IntegrityError) as e:
            last_error = e
            time.sleep(0.5)
    raise RuntimeError(f"init_db failed after {max_retries} attempts: {last_error}")
