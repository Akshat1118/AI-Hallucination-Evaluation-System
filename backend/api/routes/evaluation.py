"""
Evaluation API routes — M1.3 Evaluation Input Module.
Handles submission, retrieval, and listing of evaluations.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from db.models import get_db, EvaluationSubmission, EvaluationResult
from services.evaluation_service import EvaluationService

router = APIRouter()


# ---------------------------------------------------------------------------
# Pydantic Schemas — M1.3: Input validation
# ---------------------------------------------------------------------------
class EvaluationRequest(BaseModel):
    """
    Evaluation submission schema.
    Supports question + AI response as primary inputs,
    with optional reference answer and source document.
    """
    question: str = Field(
        ...,
        min_length=5,
        max_length=5000,
        description="The question or prompt given to the AI system",
        examples=["What is the capital of France?"],
    )
    ai_response: str = Field(
        ...,
        min_length=1,
        max_length=20000,
        description="The AI-generated response to evaluate",
        examples=["The capital of France is Paris."],
    )
    reference_answer: Optional[str] = Field(
        default=None,
        max_length=20000,
        description="Optional ground-truth reference answer for comparison",
    )
    source_document: Optional[str] = Field(
        default=None,
        max_length=50000,
        description="Optional source document or reference material for grounding",
    )
    dataset_source: Optional[str] = Field(
        default="user",
        description="Origin of this evaluation (user | truthful_qa | squad)",
    )

    @field_validator("question", "ai_response")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Field cannot be blank.")
        return stripped

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "What is the boiling point of water?",
                    "ai_response": "Water boils at 100 degrees Celsius (212°F) at sea level.",
                    "reference_answer": "The boiling point of water is 100°C (212°F) at standard atmospheric pressure.",
                }
            ]
        }
    }


class EvaluationResponse(BaseModel):
    """Response returned after submission."""
    evaluation_id: str
    status: str
    message: str


class EvaluationResultResponse(BaseModel):
    """Full evaluation result schema."""
    evaluation_id: str
    submission_id: str
    question: str
    ai_response: str
    scores: dict
    overall_score: Optional[float]
    verdict: Optional[str]
    retrieved_context: Optional[list]
    status: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@router.post("/evaluate", response_model=EvaluationResponse, status_code=202)
async def submit_evaluation(
    request: EvaluationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Submit an AI response for evaluation.

    - **question**: The original question (required)
    - **ai_response**: The AI-generated answer to evaluate (required)
    - **reference_answer**: Ground-truth answer for comparison (optional)
    - **source_document**: Reference material for grounding (optional)

    Returns an `evaluation_id` to poll for results.
    """
    # Create submission record
    submission = EvaluationSubmission(
        id=str(uuid.uuid4()),
        question=request.question,
        ai_response=request.ai_response,
        reference_answer=request.reference_answer,
        source_document=request.source_document,
        dataset_source=request.dataset_source or "user",
        status="pending",
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    # Trigger background evaluation pipeline
    background_tasks.add_task(
        EvaluationService.run_evaluation_pipeline,
        submission_id=submission.id,
        question=request.question,
        ai_response=request.ai_response,
        reference_answer=request.reference_answer,
        source_document=request.source_document,
    )

    return EvaluationResponse(
        evaluation_id=submission.id,
        status="pending",
        message="Evaluation submitted successfully. Poll /evaluate/{id} for results.",
    )


@router.get("/evaluate/{evaluation_id}", response_model=EvaluationResultResponse)
async def get_evaluation_result(
    evaluation_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve evaluation result by ID.
    Poll this endpoint after submitting an evaluation.
    """
    # Look up submission
    stmt = select(EvaluationSubmission).where(EvaluationSubmission.id == evaluation_id)
    result = await db.execute(stmt)
    submission = result.scalar_one_or_none()

    if not submission:
        raise HTTPException(status_code=404, detail=f"Evaluation {evaluation_id} not found.")

    # Look up result
    r_stmt = select(EvaluationResult).where(EvaluationResult.submission_id == evaluation_id)
    r_result = await db.execute(r_stmt)
    eval_result = r_result.scalar_one_or_none()

    scores = {}
    overall_score = None
    verdict = None
    retrieved_context = None

    if eval_result:
        scores = {
            "relevance": {
                "score": eval_result.relevance_score,
                "reasoning": eval_result.relevance_reasoning,
            },
            "accuracy": {
                "score": eval_result.accuracy_score,
                "reasoning": eval_result.accuracy_reasoning,
            },
            "hallucination": {
                "score": eval_result.hallucination_score,
                "severity": eval_result.hallucination_severity,
                "reasoning": eval_result.hallucination_reasoning,
                "hallucinated_segments": eval_result.hallucinated_segments,
            },
            "completeness": {
                "score": eval_result.completeness_score,
                "reasoning": eval_result.completeness_reasoning,
            },
        }
        overall_score = eval_result.overall_score
        verdict = eval_result.verdict
        retrieved_context = eval_result.retrieved_context

    return EvaluationResultResponse(
        evaluation_id=evaluation_id,
        submission_id=submission.id,
        question=submission.question,
        ai_response=submission.ai_response,
        scores=scores,
        overall_score=overall_score,
        verdict=verdict,
        retrieved_context=retrieved_context,
        status=submission.status,
    )


@router.get("/evaluations", response_model=list[EvaluationResponse])
async def list_evaluations(
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """List recent evaluation submissions."""
    stmt = select(EvaluationSubmission).order_by(
        EvaluationSubmission.created_at.desc()
    ).limit(limit).offset(offset)
    result = await db.execute(stmt)
    submissions = result.scalars().all()

    return [
        EvaluationResponse(
            evaluation_id=s.id,
            status=s.status,
            message=f"Submitted at {s.created_at}",
        )
        for s in submissions
    ]
