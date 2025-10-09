from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapers.indeed_scraper import IndeedScraper


def init_webdriver():
    chrome_options = Options()

    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)

    return driver


if __name__ == "__main__":
    scraper = IndeedScraper("student software", "israel")
    
    driver = init_webdriver()

    for job in scraper.fetch(driver):
        print(f"{job[0]} - {job[1]}")

    driver.quit()