from typing import Generator, Tuple, Dict
from selenium import webdriver
from bs4 import BeautifulSoup


class IndeedScraper:
    def __init__(self, title: str, location: str) -> None:
        title = title.replace(" ", "+")
        location = location.replace(" ", "+")
        self.search_url = f"https://il.indeed.com/jobs?q={title}&l={location}"


    def fetch(self, driver: webdriver.Chrome) -> Generator[Tuple[str, str], None, None]:
        driver.get(self.search_url)

        html_source = driver.page_source
        soup = BeautifulSoup(html_source, "html.parser")

        print(soup)

        for job in soup.find_all("div", attrs={"data-testid": "slider_item"}):
            job_title = job.find("a").text.strip()
            company_name = job.find("span", {"data-testid": "company-name"}).text.strip()
            yield job_title, company_name