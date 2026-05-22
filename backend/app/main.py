from fastapi import FastAPI

from app.api.applications import router as applications_router
from app.api.auth import router as auth_router
from app.api.health import router as health_router

app = FastAPI(
    title="Career Copilot API",
    version="0.1.0",
    description="Backend API for the Career Copilot portfolio project.",
)

app.include_router(applications_router)
app.include_router(auth_router)
app.include_router(health_router)
