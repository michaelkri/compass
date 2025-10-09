from typing import List
from selenium import webdriver
from bs4 import BeautifulSoup
from core.db import Job


class IndeedScraper:
    def __init__(self, title: str, location: str) -> None:
        title = title.replace(" ", "+")
        location = location.replace(" ", "+")
        self.search_url = f"https://il.indeed.com/jobs?q={title}&l={location}"


    def fetch(self, driver: webdriver.Chrome) -> List[Job]:
        driver.get(self.search_url)

        html_source = driver.page_source
        soup = BeautifulSoup(html_source, "html.parser")

        jobs = []
        for job_entry in soup.find_all("div", attrs={"data-testid": "slider_item"}):
            job_title = job_entry.find("a").text.strip()
            company_name = job_entry.find("span", {"data-testid": "company-name"}).text.strip()
            
            job_id = job_entry.find("a").get("id")[4:]
            job_url = f"https://il.indeed.com/viewjob?jk={job_id}"

            job = Job(title=job_title, company=company_name, url=job_url)

            jobs.append(job)

        return jobs