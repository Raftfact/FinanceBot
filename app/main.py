from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.router import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Finance Tracker API starting...")
    yield
    print("👋 Finance Tracker API shutting down...")


app = FastAPI(
    title="Finance Tracker API",
    description="Backend API for personal finance tracking",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "finance-tracker-api"}