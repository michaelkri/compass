from typing import List
from selenium import webdriver
from bs4 import BeautifulSoup
from trafilatura import extract
from core.models import Job


class IndeedScraper:
    def __init__(self, title: str, location: str) -> None:
        title = title.replace(" ", "+")
        location = location.replace(" ", "+")
        self.search_url = f"https://il.indeed.com/jobs?q={title}&l={location}"


    def fetch_jobs(self, driver: webdriver.Chrome) -> List[Job]:
        driver.get(self.search_url)

        html_source = driver.page_source
        soup = BeautifulSoup(html_source, "html.parser")

        jobs = []
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

        return jobs
    

    @staticmethod
    def fetch_description(url: str, driver: webdriver.Chrome) -> str:
        driver.get(url)

        html_source = driver.page_source
        soup = BeautifulSoup(html_source, "html.parser")

        description_html = soup.find("div", {"id": "jobDescriptionText"})
        description = "".join([str(tag) for tag in description_html.children])
        return description