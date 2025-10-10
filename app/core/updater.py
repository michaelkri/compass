from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapers import ALL_SCRAPERS
from sqlalchemy.orm import Session
from .db import get_db_session
from .models import Job


def init_webdriver():
    chrome_options = Options()

    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def run_update() -> None:
    driver = init_webdriver()
    
    for scraper in ALL_SCRAPERS:
        scpr = scraper("student software", "israel")

        with get_db_session() as db:
            for job in scpr.fetch(driver):
                db.add(job)
                db.commit()

    driver.quit()


def fetch_job_description(job_id: int) -> Optional[str]:
    return ""


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