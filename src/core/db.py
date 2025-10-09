from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .models import Base, Job


DATABASE_URL = "sqlite:///jobs.db"


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_database_tables():
    Base.metadata.create_all(engine)


@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db():
    with get_db_session() as db:
        yield db