import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyses import router as analyses_router
from app.api.applications import router as applications_router
from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.interviews import router as interviews_router
from app.api.resumes import router as resumes_router

BACKEND_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BACKEND_DIR / ".env")

DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


def get_cors_origins() -> list[str]:
    configured_origins = os.getenv("BACKEND_CORS_ORIGINS")

    if not configured_origins:
        return DEFAULT_CORS_ORIGINS

    return [
        origin.strip()
        for origin in configured_origins.split(",")
        if origin.strip()
    ]


app = FastAPI(
    title="Career Copilot API",
    version="0.1.0",
    description="Backend API for the Career Copilot portfolio project.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyses_router)
app.include_router(applications_router)
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(interviews_router)
app.include_router(resumes_router)
