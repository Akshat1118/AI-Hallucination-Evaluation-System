"""
Knowledge Base API routes — M1.4.
Manage dataset ingestion, embedding, and retrieval.
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional

from services.kb_service import KnowledgeBaseService

router = APIRouter()


class IngestRequest(BaseModel):
    dataset: str = "all"           # "truthful_qa" | "squad" | "all"
    max_samples: Optional[int] = 500


class RetrievalRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/knowledge-base/ingest", status_code=202)
async def ingest_datasets(
    request: IngestRequest,
    background_tasks: BackgroundTasks,
):
    """
    Trigger ingestion of benchmark datasets (TruthfulQA and/or SQuAD).
    Runs in the background — chunking, embedding, and indexing into ChromaDB.
    """
    background_tasks.add_task(
        KnowledgeBaseService.ingest,
        dataset=request.dataset,
        max_samples=request.max_samples,
    )
    return {
        "status": "ingestion_started",
        "dataset": request.dataset,
        "message": f"Ingesting {request.dataset} dataset(s) in background.",
    }


@router.post("/knowledge-base/retrieve")
async def retrieve_context(request: RetrievalRequest):
    """
    Retrieve relevant chunks from the knowledge base for a given query.
    Used to test retrieval quality (M1.4 validation).
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    results = await KnowledgeBaseService.retrieve(
        query=request.query,
        top_k=request.top_k,
    )
    return {
        "query": request.query,
        "results": results,
        "count": len(results),
    }


@router.get("/knowledge-base/stats")
async def knowledge_base_stats():
    """Get knowledge base statistics (count of indexed documents)."""
    stats = await KnowledgeBaseService.get_stats()
    return stats
