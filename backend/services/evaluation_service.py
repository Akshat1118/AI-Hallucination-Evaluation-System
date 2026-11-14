"""
Evaluation Service — coordinates the evaluation pipeline with RAG retrieval.
Called by the FastAPI background task system.
"""
from typing import Optional
import asyncio

from core.orchestrator import EvaluationOrchestrator
from services.kb_service import KnowledgeBaseService
from db.models import AsyncSessionLocal, EvaluationSubmission, EvaluationResult
from sqlalchemy import select, update
import uuid


class EvaluationService:
    """Business logic layer for running evaluations end-to-end."""

    @staticmethod
    async def run_evaluation_pipeline(
        submission_id: str,
        question: str,
        ai_response: str,
        reference_answer: Optional[str] = None,
        source_document: Optional[str] = None,
    ):
        """
        Full evaluation pipeline:
        1. Update submission status to 'processing'
        2. Retrieve relevant context via RAG
        3. Run multi-agent evaluation
        4. Store results
        5. Update submission status to 'completed'
        """
        async with AsyncSessionLocal() as db:
            # Mark as processing
            await db.execute(
                update(EvaluationSubmission)
                .where(EvaluationSubmission.id == submission_id)
                .values(status="processing")
            )
            await db.commit()

            try:
                # Step 1: RAG retrieval
                retrieved = await KnowledgeBaseService.retrieve(
                    query=question, top_k=5
                )
                context_texts = [r["document"] for r in retrieved]

                # Step 2: Merge source_document into context if provided
                if source_document:
                    context_texts.insert(0, source_document)

                # Step 3: Run orchestrator
                orchestrator = EvaluationOrchestrator()
                eval_output = await orchestrator.evaluate(
                    question=question,
                    ai_response=ai_response,
                    reference_answer=reference_answer,
                    source_document=source_document,
                    retrieved_context=context_texts,
                )

                # Step 4: Store results
                h = eval_output["hallucination"]
                result = EvaluationResult(
                    id=str(uuid.uuid4()),
                    submission_id=submission_id,
                    relevance_score=eval_output["relevance"].get("score"),
                    relevance_reasoning=eval_output["relevance"].get("reasoning"),
                    accuracy_score=eval_output["accuracy"].get("score"),
                    accuracy_reasoning=eval_output["accuracy"].get("reasoning"),
                    hallucination_score=h.get("score"),
                    hallucination_severity=h.get("severity"),
                    hallucination_reasoning=h.get("reasoning"),
                    hallucinated_segments=h.get("hallucinated_segments"),
                    completeness_score=eval_output["completeness"].get("score"),
                    completeness_reasoning=eval_output["completeness"].get("reasoning"),
                    overall_score=eval_output["overall_score"],
                    verdict=eval_output["verdict"],
                    retrieved_context=context_texts[:5],
                )
                db.add(result)

                # Step 5: Mark as completed
                await db.execute(
                    update(EvaluationSubmission)
                    .where(EvaluationSubmission.id == submission_id)
                    .values(status="completed")
                )
                await db.commit()

            except Exception as e:
                await db.execute(
                    update(EvaluationSubmission)
                    .where(EvaluationSubmission.id == submission_id)
                    .values(status="failed")
                )
                await db.commit()
                raise e
