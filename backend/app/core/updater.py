from contextlib import contextmanager
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy.orm import Session
from scrapers import ALL_SCRAPERS, IndeedScraper
from .db import get_db_session
from .models import Job, AIAnalysis, Insight
from services.job_analysis import create_ai_analysis


@contextmanager
def create_webdriver():
    chrome_options = Options()

    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    try:
        driver = webdriver.Chrome(options=chrome_options)
        yield driver
    finally:
        driver.quit()


def run_update() -> None:
    with create_webdriver() as driver:
        for scraper in ALL_SCRAPERS:
            scpr = scraper("student software", "israel")
            with get_db_session() as db:
                for job in scpr.fetch_jobs(driver):
                    db.add(job)
                    db.commit()


def fetch_job_description(job_source: str, job_url: str) -> Optional[str]:
    with create_webdriver() as driver:
        if job_source == "Indeed":
            return IndeedScraper.fetch_description(job_url, driver)
    
    return ""


def get_or_create_job_description(db: Session, job_id: int) -> Optional[Job]:
    # Try to get job from database
    job = db.query(Job).filter_by(id=job_id).first()

    # Job not found in database
    if not job:
        return None
    
    # Previously fetched job description
    if job.description:
        return job
    
    # Description not saved yet: get from web
    fetched_description = fetch_job_description(job.source, job.url)

    # Save fetched description in database
    job.description = fetched_description
    
    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_or_create_ai_analysis(db: Session, job_id: int) -> Optional[AIAnalysis]:
    # Temporary
    RESUME_CONTENT = """
John Doe
123 Main St, Citytown, ST 12345
(123) 456-7890
johndoe@email.com

EDUCATION
Bachelor of Science in Computer Science
University of Citytown, Anytown, ST
Expected Graduation: May 2025

Relevant Courses:

    Data Structures and Algorithms
    Database Management Systems
    Web Development
    Operating Systems
    Software Engineering

SKILLS

    Programming Languages: Python, Java, C++
    Web Technologies: HTML, CSS, JavaScript, React
    Database: SQL, MySQL
    Version Control: Git
    Agile Methodologies

PROJECTS

    Personal Portfolio Website
        Developed a responsive portfolio website using HTML/CSS, showcasing personal projects and skills.
        Implemented basic JavaScript functionality for improved user experience.

    Basic Chat Application
        Created a simple chat application using Python and Flask.
        Enabled real-time communication with WebSocket integration.

    Todo List Application
        Built a full-stack todo list application using React for frontend and Node.js for backend.
        Implemented user authentication and local storage for tasks.

EXTRACURRICULARS

    Member, University Coding Club (2022 - Present)
    Volunteer, Local Tech Community Workshops (2023)

INTERESTS

    Artificial Intelligence
    Open Source Contributions
    Competitive Programming
"""
   
    
    # Try to get job from database
    job = db.query(Job).filter_by(id=job_id).first()

    # Job not found in database
    if not job:
        return None
    
    # Already created analysis
    if job.analysis:
        return job.analysis
    
    # Create the analysis
    analysis_schema = create_ai_analysis(job.description, RESUME_CONTENT)

    # Convert generated insights from schemas to ORM models
    insights = []
    for insight_schema in analysis_schema.insights_list:
        insight_model = Insight(
            title=insight_schema.title,
            category=insight_schema.category,
            requirement=insight_schema.requirement,
            candidate_fact=insight_schema.candidate_fact,
            summary=insight_schema.summary
        )
        insights.append(insight_model)

    # Define the analysis for this job
    job_analysis = AIAnalysis(
        candidate_fit_score=analysis_schema.candidate_fit_score,
        application_summary=analysis_schema.application_summary,
        top_strengths=analysis_schema.top_strengths,
        key_gaps=analysis_schema.key_gaps,
        quick_impact_skills=analysis_schema.quick_impact_skills,
        insights_list=insights,
        job_id=job.id
    )

    # Store analysis for future access
    job.analysis = job_analysis

    db.add(job_analysis)
    db.commit()
    db.refresh(job_analysis)

    return job_analysis