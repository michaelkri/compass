from contextlib import contextmanager
from pathlib import Path
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy.orm import Session
from scrapers import ALL_SCRAPERS, IndeedScraper
from scrapers.linkedin_scraper import LinkedInScraper
from .db import get_db_session
from .models import Job, AIAnalysis, Insight
from services.job_analysis import create_ai_analysis


@contextmanager
def _create_webdriver():
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


def scrape_jobs(db: Session) -> None:
    added_count = 0

    with _create_webdriver() as driver:
        for scraper in ALL_SCRAPERS:
            current_scraper = scraper("student software", "israel")
            for job in current_scraper.fetch_jobs(driver):
                try:
                    db.add(job)
                    db.commit()
                    added_count += 1
                except Exception as e:
                    print(f"Failed to add scraped job: {e.args}")

    return added_count


def fetch_job_description(job_source: str, job_url: str) -> Optional[str]:
    with _create_webdriver() as driver:
        if job_source == "Indeed":
            return IndeedScraper.fetch_description(job_url, driver)
        elif job_source == "LinkedIn":
            return LinkedInScraper.fetch_description(job_url, driver)
    
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


def get_or_create_ai_analysis(db: Session, job_id: int, base_dir: Path) -> Optional[AIAnalysis]:
    # Try to get job from database
    job = db.query(Job).filter_by(id=job_id).first()

    # Job not found in database
    if not job:
        return None
    
    # Already created analysis
    if job.analysis:
        return job.analysis
    
    # Create the analysis
    analysis_schema = create_ai_analysis(job.description, base_dir)

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
        possible_questions=analysis_schema.possible_questions,
        insights_list=insights,
        job_id=job.id
    )

    # Store analysis for future access
    job.analysis = job_analysis

    db.add(job_analysis)
    db.commit()
    db.refresh(job_analysis)

    return job_analysis