from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(Text)
    company: str = Column(Text)
    location: str = Column(Text)
    url: str = Column(Text)
    description: str = Column(Text, nullable=True)