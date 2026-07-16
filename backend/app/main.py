"""LifeOS Backend — AI Personal Operating System."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import api_router
from app.telegram.mini_app import router as telegram_router
from app.database.session import engine

app = FastAPI(
    title="LifeOS API",
    description="AI Personal Operating System — Backend API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(api_router, prefix="/api/v1")

# Telegram routes
app.include_router(telegram_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "lifeos-api"}
