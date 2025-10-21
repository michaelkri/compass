from abc import abstractmethod, ABC
from typing import List
from selenium import webdriver
from app.core.models import Job



class BaseScraper(ABC):
    def __init__(self, titles: List[str], location: str) -> None:
        self.titles = [title.replace(" ", "+") for title in titles]
        self.location = location.replace(" ", "+")


    @abstractmethod
    def fetch_jobs(self, driver: webdriver.Chrome) -> List[Job]:
        pass


    @staticmethod
    @abstractmethod
    def fetch_description(url: str, driver: webdriver.Chrome) -> str:
        pass