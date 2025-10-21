from contextlib import asynccontextmanager
from typing import List
from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from app.core.db import get_db, create_db_tables
from app.core.models import Job, SearchTerm
from app.core.schemas import AnalysisSchema, JobCreate, JobSchema, SearchTermCreate, SearchTermSchema
from app.core.updater import get_or_create_ai_analysis, scrape_jobs, get_or_create_job_description


BASE_DIR = Path(__file__).resolve().parent.parent

# templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()

    create_db_tables()

    try:
        scheduler.add_job(
            func=scrape_jobs,
            args=get_db(),
            trigger=CronTrigger(hour='8,11,14,17'),
            id='scraper_job', 
            name='Periodic Job Scraper',
            replace_existing=True,
            misfire_grace_time=600
        )

        scheduler.start()
        print("Scheduler started.")

    except Exception as e:
        print(f"Error starting scheduler: {e}")

    yield

    scheduler.shutdown()


app = FastAPI(
    title="Compass",
    lifespan=lifespan
)


# app.mount(
#     "/static",
#     StaticFiles(directory=str(BASE_DIR / "backend" / "app" / "static")),
#     name="static"
# )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/", response_class=HTMLResponse)
# async def read_root(
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     jobs = db.query(Job).limit(50).all()

#     context = {
#         "request": request, 
#         "jobs": jobs
#     }

#     return templates.TemplateResponse(
#         name="index.html",
#         context=context
#     )


@app.post("/api/jobs/update", status_code=200)
async def update_jobs(
    db: Session = Depends(get_db)
):
    added_count = scrape_jobs(db)
    return {
        "status": "success",
        "new_items_count": added_count
    }


@app.get("/api/jobs", response_model=List[JobSchema])
async def read_jobs(
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).all()
    return jobs


@app.post("/api/jobs", response_model=JobSchema, status_code=201)
async def create_job(
    job: JobCreate,
    db: Session = Depends(get_db)
):
    new_job = Job(**job.model_dump())
    db.add(new_job)
    db.commit()
    return new_job


@app.get("/api/jobs/{job_id}", response_model=JobSchema)
async def get_job_content(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = get_or_create_job_description(db, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found.")
    
    return job


@app.delete("/api/jobs/{job_id}", status_code=204)
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    try:
        job_to_delete = db.query(Job).filter_by(id=job_id).first()
        db.delete(job_to_delete)
        db.commit()
    except:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found.")
        
    return


@app.get("/api/analysis/{job_id}", response_model=AnalysisSchema)
async def get_job_analysis(
    job_id: int,
    db: Session = Depends(get_db)
):
    try:
        analysis = get_or_create_ai_analysis(db, job_id, BASE_DIR)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Could not get AI analysis for job with ID {job_id}.")

    if analysis is None:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found.")
    
    return analysis


@app.get("/api/search_terms", response_model=List[SearchTermSchema])
async def get_search_terms(
    db: Session = Depends(get_db)
):
    terms = db.query(SearchTerm).all()
    return terms


@app.post("/api/search_terms", response_model=SearchTermSchema, status_code=201)
async def create_search_term(
    term: SearchTermCreate,
    db: Session = Depends(get_db)
):
    new_term = SearchTerm(**term.model_dump())
    db.add(new_term)
    db.commit()
    return new_term
  

@app.delete("/api/search_terms/{term_id}", status_code=204)
async def delete_search_term(
    term_id: int,
    db: Session = Depends(get_db)
):
    term_to_delete = db.query(SearchTerm).filter_by(id=term_id).first()
    db.delete(term_to_delete)
    db.commit()
    return


# @app.get("{full_path:path}")
# async def serve_spa(full_path: str):
#     index_path = BASE_DIR / "frontend" / "build" / "index.html"
#     if index_path.exists():
#         return FileResponse(index_path)
#     else:
#         return HTMLResponse(content="<h1>Index file not found</h1>", status_code=404)