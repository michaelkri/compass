from sqlalchemy import Column, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Job(Base):
    __tablename__ = "job"

    title: str = Column(Text)
    company: str = Column(Text)
    url: str = Column(Text, primary_key=True)