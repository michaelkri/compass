from typing import Annotated, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


class InsightSchema(BaseModel):
    """A single, actionable insight comparing a job requirement and your resume."""

    model_config = ConfigDict(from_attributes=True)

    title: str = Field(
        description="Title for this insight"
    )

    category: Literal["Match", "Missing", "Partial", "Quick Learn"] = Field(
        description="The type of comparison: 'Match', 'Missing', 'Partial', or 'Quick Learn' (for a highly beneficial, easy-to-acquire skill)."
    )

    requirement: str = Field(
        description="The specific requirement or responsibility from the Job Description that this insight addresses."
    )

    candidate_fact: Optional[str] = Field(
        default=None,
        description="The corresponding fact or skill from the Resume that supports the insight."
    )

    summary: str = Field(
        description="A concise, human-readable insight statement."
    )


class AnalysisSchema(BaseModel):
    """A comprehensive analysis of how your resume aligns with this job, 
    with actionable advice to improve your application."""

    model_config = ConfigDict(from_attributes=True)

    candidate_fit_score: Annotated[int, Field(ge=0, le=100)] = Field(
        description="A score from 0 to 100 representing the overall fit of the candidate for the job."
    )

    application_summary: str = Field(
        description="A brief, 2-3 sentence summary of the candidate's fit for the role, written to provide a high-level takeaway."
    )

    top_strengths: List[str] = Field(
        description="3-5 key strengths of the candidate based on the analysis."
    )

    key_gaps: List[str] = Field(
        description="3-5 critical areas where the candidate is missing a core requirement."
    )

    possible_questions: List[str] = Field(
        description="3-5 possible interview questions the candidate may be asked on."
    )

    insights_list: List[InsightSchema] = Field(
        description="A comprehensive list of all generated insights."
    )


class JobSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: str
    location: str
    url: str
    description: str
    source: str

    analysis: AnalysisSchema | None


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    url: str
    description: str
    source: str


class SearchTermSchema(BaseModel):
    id: int
    term: str


class SearchTermCreate(BaseModel):
    term: str