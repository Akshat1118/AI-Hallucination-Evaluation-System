"""
Evaluation Orchestrator — coordinates all judge agents and aggregates scores.
M1.2 — Agent Orchestration
"""
from typing import Optional
import asyncio

from agents.relevance_agent import RelevanceJudgeAgent
from agents.accuracy_agent import AccuracyJudgeAgent
from agents.hallucination_agent import HallucinationDetectionAgent
from agents.completeness_agent import CompletenessJudgeAgent
from agents.verdict_agent import VerdictAgent
from core.config import settings


class EvaluationOrchestrator:
    """
    Orchestrates the multi-agent evaluation pipeline.

    Flow:
      1. RAG retrieval — fetch relevant context from knowledge base
      2. Run judge agents in parallel (Relevance, Accuracy, Hallucination, Completeness)
      3. Aggregate scores via Verdict Agent
      4. Return structured evaluation result
    """

    def __init__(self):
        self.relevance_agent = RelevanceJudgeAgent()
        self.accuracy_agent = AccuracyJudgeAgent()
        self.hallucination_agent = HallucinationDetectionAgent()
        self.completeness_agent = CompletenessJudgeAgent()
        self.verdict_agent = VerdictAgent()

    async def evaluate(
        self,
        question: str,
        ai_response: str,
        reference_answer: Optional[str] = None,
        source_document: Optional[str] = None,
        retrieved_context: Optional[list] = None,
    ) -> dict:
        """
        Run the full evaluation pipeline.

        Args:
            question: The original question
            ai_response: The AI response to evaluate
            reference_answer: Optional ground-truth answer
            source_document: Optional reference material
            retrieved_context: Pre-fetched RAG context chunks

        Returns:
            dict with per-dimension scores, reasoning, and overall verdict
        """
        ctx = retrieved_context or []
        ctx_text = "\n\n".join(ctx) if ctx else "No reference context available."

        # Run all judge agents in parallel
        relevance_task = self.relevance_agent.evaluate(
            question=question,
            ai_response=ai_response,
            context=ctx_text,
        )
        accuracy_task = self.accuracy_agent.evaluate(
            question=question,
            ai_response=ai_response,
            reference_answer=reference_answer,
            context=ctx_text,
        )
        hallucination_task = self.hallucination_agent.evaluate(
            question=question,
            ai_response=ai_response,
            reference_answer=reference_answer,
            context=ctx_text,
        )
        completeness_task = self.completeness_agent.evaluate(
            question=question,
            ai_response=ai_response,
            reference_answer=reference_answer,
            context=ctx_text,
        )

        relevance_result, accuracy_result, hallucination_result, completeness_result = (
            await asyncio.gather(
                relevance_task,
                accuracy_task,
                hallucination_task,
                completeness_task,
            )
        )

        # Compute weighted overall score via Verdict Agent
        verdict_result = self.verdict_agent.compute_verdict(
            relevance=relevance_result,
            accuracy=accuracy_result,
            hallucination=hallucination_result,
            completeness=completeness_result,
        )

        return {
            "relevance": relevance_result,
            "accuracy": accuracy_result,
            "hallucination": hallucination_result,
            "completeness": completeness_result,
            "overall_score": verdict_result["overall_score"],
            "verdict": verdict_result["verdict"],
        }
