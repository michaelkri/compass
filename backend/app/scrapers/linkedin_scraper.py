import time
from typing import List
from selenium import webdriver
from bs4 import BeautifulSoup
from core.models import Job
from scrapers.base_scraper import BaseScraper


class LinkedInScraper(BaseScraper):
    def fetch_jobs(self, driver: webdriver.Chrome) -> List[Job]:
        jobs = []

        for job_title in self.titles:
            search_url = f"https://il.linkedin.com/jobs/search?keywords={job_title}&location={self.location}&f_TPR=r604800"
            
            driver.get(search_url)

            html_source = driver.page_source
            soup = BeautifulSoup(html_source, "html.parser")

            for job_entry in soup.find_all("div", class_="job-search-card"):
                job_title = job_entry.find("a").text.strip()
                company_name = job_entry.find("h4", class_="base-search-card__subtitle").text.strip()
                location = job_entry.find("span", class_="job-search-card__location").text.strip()
                
                job_id = job_entry.get("data-entity-urn")[18:]
                job_url = f"https://il.linkedin.com/jobs/view/{job_id}"

                job = Job(
                    title=job_title,
                    company=company_name,
                    location=location,
                    url=job_url,
                    source="LinkedIn"
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

        description_html = soup.find("div", class_="description__text").find("div", class_="show-more-less-html__markup")
        description = "".join([str(tag) for tag in description_html.children])
        return description