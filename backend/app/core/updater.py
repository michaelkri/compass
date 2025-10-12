from contextlib import contextmanager
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapers import ALL_SCRAPERS, IndeedScraper
from sqlalchemy.orm import Session
from .db import get_db_session
from .models import Job


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