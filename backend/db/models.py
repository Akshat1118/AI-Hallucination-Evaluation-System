"""
SQLAlchemy database models for evaluation submissions and results.
"""
from sqlalchemy import Column, String, Float, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime, timezone
import uuid

from core.config import settings


# ---------------------------------------------------------------------------
# Engine & Session
# ---------------------------------------------------------------------------
engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    """FastAPI dependency — yields a database session."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    """Create all tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class EvaluationSubmission(Base):
    """Stores raw evaluation input submissions."""
    __tablename__ = "evaluation_submissions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    reference_answer = Column(Text, nullable=True)
    source_document = Column(Text, nullable=True)
    dataset_source = Column(String, nullable=True)        # e.g. "truthful_qa", "squad", "user"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="pending")            # pending | processing | completed | failed


class EvaluationResult(Base):
    """Stores structured evaluation results from the agent pipeline."""
    __tablename__ = "evaluation_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    submission_id = Column(String, nullable=False)

    # Scores (0–10 per dimension)
    relevance_score = Column(Float, nullable=True)
    relevance_reasoning = Column(Text, nullable=True)

    accuracy_score = Column(Float, nullable=True)
    accuracy_reasoning = Column(Text, nullable=True)

    hallucination_score = Column(Float, nullable=True)
    hallucination_severity = Column(String, nullable=True)   # NONE | MINOR | MODERATE | SEVERE | CRITICAL
    hallucination_reasoning = Column(Text, nullable=True)
    hallucinated_segments = Column(JSON, nullable=True)

    completeness_score = Column(Float, nullable=True)
    completeness_reasoning = Column(Text, nullable=True)

    overall_score = Column(Float, nullable=True)
    verdict = Column(String, nullable=True)                  # EXCELLENT | GOOD | ACCEPTABLE | POOR | DANGEROUS

    # RAG context used
    retrieved_context = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class KnowledgeBaseEntry(Base):
    """Tracks indexed knowledge base entries."""
    __tablename__ = "knowledge_base_entries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset = Column(String, nullable=False)      # truthful_qa | squad
    question = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
    context = Column(Text, nullable=True)
    chunk_id = Column(String, nullable=True)      # ChromaDB chunk ID
    embedded = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
