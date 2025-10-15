from typing import Annotated, List, Literal, Optional
from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship
from .db import Base


class Job(Base):
    __tablename__ = "job"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(Text)
    company: str = Column(Text)
    location: str = Column(Text)
    url: str = Column(Text)
    description: str = Column(Text, nullable=True)
    source: str = Column(Text)
    
    analysis: Mapped["AIAnalysis"] = relationship(back_populates="job")


class Insight(Base):
    __tablename__ = "insight"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id: int = Column(Integer, ForeignKey("analysis.id"))

    title: str = Column(String)
    category: Literal["Match", "Missing", "Partial", "Exceeding", "Quick Learn"] = Column(String)
    requirement: str = Column(String)
    candidate_fact: Optional[str] = Column(String, nullable=True)
    summary: str = Column(String)

    analysis: Mapped["AIAnalysis"] = relationship(back_populates="insights_list")


class AIAnalysis(Base):
    __tablename__ = "analysis"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    job_id: int = Column(Integer, ForeignKey("job.id"))

    candidate_fit_score: int = Column(Integer)
    application_summary: str = Column(String)
    top_strengths: List[str] = Column(JSON)
    key_gaps: List[str] = Column(JSON)
    quick_impact_skills: List[str] = Column(JSON)
    
    insights_list: Mapped[List["Insight"]] = relationship(back_populates="analysis")
    job: Mapped["Job"] = relationship(back_populates="analysis")