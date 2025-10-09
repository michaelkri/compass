from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapers import ALL_SCRAPERS


def init_webdriver():
    chrome_options = Options()

    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def run_update():
    driver = init_webdriver()
    
    for scraper in ALL_SCRAPERS:
        scpr = scraper("student software", "israel")

        for job in scpr.fetch(driver):
            print(f"{job.title} - {job.company} - {job.url}")

    driver.quit()