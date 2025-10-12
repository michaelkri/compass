from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from core.db import get_db, create_db_tables
from core.models import Job
from core.schemas import JobSchema
from core.updater import run_update, get_or_create_job_description


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()

    try:
        # scheduler.add_job(
        #     func=run_update, 
        #     trigger=CronTrigger(hour='8,11,14,17'),
        #     id='scraper_job', 
        #     name='Periodic Job Scraper',
        #     replace_existing=True,
        #     misfire_grace_time=600
        # )

        scheduler.start()
        print("Scheduler started.")

    except Exception as e:
        print(f"Error starting scheduler: {e}")

    yield

    scheduler.shutdown()


app = FastAPI(
    title="Vantage",
    lifespan=lifespan
)


app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


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


@app.get("/api/jobs")
async def read_jobs(
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).limit(50).all()

    return {
        "jobs": jobs
    }


@app.get("/api/job/{job_id}", response_model=JobSchema)
async def get_job_content(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = get_or_create_job_description(db, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found.")
    
    return job


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)