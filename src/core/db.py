from typing import List, Optional
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, Job
from .updater import fetch_job_description


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


def fetch_job_summaries(db: Session) -> List[Job]:
    return db.query(Job).limit(50).all()


def get_or_create_job_description(db: Session, job_id: int) -> Optional[Job]:
    # Try to get job from database
    job = db.query(Job).filter(Job.url == job_id).first()

    # Job not found in database
    if not job:
        return None
    
    # Previously fetched job description
    if job.description:
        return job
    
    # Description not saved yet: get from web
    fetched_description = fetch_job_description(job_id)

    # Save fetched description in database
    job.description = fetched_description
    
    db.add(job)
    db.commit()
    db.refresh(job)

    return job