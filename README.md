# Compass - AI-Powered Job-Fit Analysis Platform

<p align="center">
    <a href="https://youtu.be/WpPG01IZOdQ">
        <strong>View demo video >></strong>
    </a>
</p>


## Overview
The server periodically scrapes jobs from various sources using Selenium.
The job titles to search for are given by the user in the settings page and saved in the database.

The scraped jobs are displayed in a forntend interface built with SvelteKit and TailwindCSS.
Clicking a job for the first time triggers the server to fetch its description (requirements) from the source website, and store it in the database.
Subsequent accesses use the stored description in the database for speed.

An AI analysis can be generated for each job, comparing the user's uploaded resume with the requirements stated in the job's description.
The analysis is created using a structured LangChain LLM with Google Gemini.
The analysis includes the following fields:
- Overall score in the range 0-100 describing the overall fit of the candidate to the job, based on their resume.
- Top Strengths
- Key gaps
- Insights: The LLM tries to extract every specific requirement in the job and for each of these

    1. Categorize whether the user fulfills this requirement, it is missing or partially fulfilled.
    2. Quote the relevant portions of both the job description and the resume (when applicable), for manual verification.
    
    Each insight is accompanied with a clear title and summary.
    Some insights are categorized as "Quick Learn": These are job requirements that are missing from the resume, but can be learned fairly quickly if needed.

Jobs can be added manually, in case the user is interested in an analysis for a job that couldn't be scraped automatically.


## Tech Stack
- **Backend:** FastAPI, Uvicorn
- **Frontend:** SvelteKit, TailwindCSS
- **ML:** LangChain
- **Web Scraping:** Selenium, BeautifulSoup
- **Database:** SQLAlchemy, SQLite


## Local Setup
Create an `.env` file with your Gemini API key:
```
GOOGLE_API_KEY=
```

Then run using Docker:
```
docker compose up --build
```