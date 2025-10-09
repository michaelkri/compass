from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from core.db import get_db, create_tables
from core.models import Job
from src.core.updater import run_update


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables if needed
    create_tables()

    try:
        scheduler.add_job(
            func=run_update, 
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
    title="Vantage",
    lifespan=lifespan
)


app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
async def dashboard_view(
    request: Request,
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).limit(50).all()

    context = {
        "request": request, 
        "jobs": jobs
    }

    return templates.TemplateResponse(
        name="index.html",
        context=context
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)