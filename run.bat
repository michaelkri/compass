@echo off


call .venv\Scripts\activate.bat


echo Starting Backend...
cd backend
start cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"


echo Starting Frontend...
cd ..\frontend && npm run dev