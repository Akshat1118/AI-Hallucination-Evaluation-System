"""Hallucination Detection Agent — identifies fabricated or unsupported claims."""
from typing import Optional
from agents.base_agent import BaseJudgeAgent


SEVERITY_MAP = {
    (9, 10): "NONE",
    (7, 8): "MINOR",
    (4, 6): "MODERATE",
    (1, 3): "SEVERE",
    (0, 0): "CRITICAL",
}


def _score_to_severity(score: float) -> str:
    score_int = int(score)
    if score_int >= 9:
        return "NONE"
    elif score_int >= 7:
        return "MINOR"
    elif score_int >= 4:
        return "MODERATE"
    elif score_int >= 1:
        return "SEVERE"
    return "CRITICAL"


class HallucinationDetectionAgent(BaseJudgeAgent):
    """
    Detects hallucinations in AI responses.
    Score: 0–10 (10 = no hallucination, 0 = completely fabricated)
    """

    async def evaluate(
        self,
        question: str,
        ai_response: str,
        reference_answer: Optional[str] = None,
        context: str = "",
    ) -> dict:
        ref_section = (
            f"REFERENCE ANSWER:\n{reference_answer}\n"
            if reference_answer
            else "REFERENCE ANSWER: Not provided.\n"
        )

        prompt = f"""You are an expert hallucination detection system for AI responses.

QUESTION:
{question}

AI RESPONSE:
{ai_response}

{ref_section}
REFERENCE CONTEXT (from knowledge base):
{context}

TASK:
Detect hallucinations — claims in the AI response that are:
- Factually false
- Not supported by the reference answer or context
- Invented or fabricated (e.g., fake citations, wrong dates, non-existent people)

IMPORTANT: Score from 0-10 where:
- 10 = NO hallucination (all claims are grounded and accurate)
- 0 = COMPLETELY fabricated (nothing can be verified)

Respond ONLY with valid JSON in this exact format:
{{
  "score": <number 0-10>,
  "reasoning": "<2-3 sentences explaining the hallucination analysis>",
  "hallucinated_segments": ["<exact phrases or sentences that are hallucinated>"],
  "unsupported_claims": ["<claims that cannot be verified from the context>"]
}}"""

        raw = await self._call_llm(prompt)
        result = self._parse_json_response(raw)
        result["dimension"] = "hallucination"
        result.setdefault("score", 5.0)
        result.setdefault("reasoning", "Could not determine hallucination level.")
        result.setdefault("hallucinated_segments", [])
        result.setdefault("unsupported_claims", [])
        result["severity"] = _score_to_severity(result.get("score", 5.0))
        return result
