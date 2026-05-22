from fastapi import FastAPI

from app.api.health import router as health_router

app = FastAPI(
    title="Career Copilot API",
    version="0.1.0",
    description="Backend API for the Career Copilot portfolio project.",
)

app.include_router(health_router)
