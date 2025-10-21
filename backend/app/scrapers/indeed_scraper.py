import time
from typing import List
from selenium import webdriver
from bs4 import BeautifulSoup
from app.core.models import Job
from app.scrapers.base_scraper import BaseScraper


class IndeedScraper(BaseScraper):
    def fetch_jobs(self, driver: webdriver.Chrome) -> List[Job]:
        jobs = []

        for job_title in self.titles:
            search_url = f"https://il.indeed.com/jobs?q={job_title}&l={self.location}"

            driver.get(search_url)

            html_source = driver.page_source
            soup = BeautifulSoup(html_source, "html.parser")

            for job_entry in soup.find_all("div", attrs={"data-testid": "slider_item"}):
                job_title = job_entry.find("a").text.strip()
                company_name = job_entry.find("span", {"data-testid": "company-name"}).text.strip()
                location = job_entry.find("div", {"data-testid": "text-location"}).text.strip()
                
                job_id = job_entry.find("a").get("id")[4:]
                job_url = f"https://il.indeed.com/viewjob?jk={job_id}"

                job = Job(
                    title=job_title,
                    company=company_name,
                    location=location,
                    url=job_url,
                    source="Indeed"
                )

                jobs.append(job)

            # Stall to avoid bot-like behavior
            time.sleep(3)

        return jobs
    

    @staticmethod
    def fetch_description(url: str, driver: webdriver.Chrome) -> str:
        driver.get(url)

        html_source = driver.page_source
        soup = BeautifulSoup(html_source, "html.parser")

        description_html = soup.find("div", {"id": "jobDescriptionText"})
        description = "".join([str(tag) for tag in description_html.children])
        return description