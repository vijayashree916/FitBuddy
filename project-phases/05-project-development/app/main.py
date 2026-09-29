import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .database import init_db
from .routes import router
from .config import SESSION_SECRET

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="Personalized 7-day fitness planning with Gemini AI.",
    version="1.0.0",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    https_only=False,
)

app.mount("/static", StaticFiles(directory=str(PROJECT_DIR / "static")), name="static")

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(router)
