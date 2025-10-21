from typing import List, Optional
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.config import DATABASE_URL


# DATABASE_NAME = "jobs.db"
# DATABASE_URL = f"sqlite:///{DATABASE_NAME}"


engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_db_tables():
    Base.metadata.create_all(engine)


@contextmanager
def get_db_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def get_db():
    with get_db_session() as db:
        yield db