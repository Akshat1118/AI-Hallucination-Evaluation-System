"""
FastAPI main application entry point.
Milestone 1 — AI Hallucination Evaluation System
"""
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_ROOT = Path(__file__).resolve().parent.parent
for p in [str(PROJECT_ROOT), str(BACKEND_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.config import settings
from db.models import init_db
from api.routes import evaluation, knowledge_base, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database on startup."""
    await init_db()
    yield


app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="Multi-agent LLM response evaluation system with RAG-grounded hallucination detection.",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS — allow React frontend dev server
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(evaluation.router, prefix="/api/v1", tags=["Evaluation"])
app.include_router(knowledge_base.router, prefix="/api/v1", tags=["Knowledge Base"])


@app.get("/")
async def root():
    return {
        "message": "AI Hallucination Evaluation System API",
        "version": settings.app_version,
        "docs": "/docs",
    }
