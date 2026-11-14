"""Accuracy Judge Agent — evaluates factual correctness of the AI response."""
from typing import Optional
from agents.base_agent import BaseJudgeAgent


class AccuracyJudgeAgent(BaseJudgeAgent):
    """
    Evaluates factual accuracy of the AI response.
    Score: 0–10 (10 = fully accurate)
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

        prompt = f"""You are evaluating the ACCURACY of an AI response.

QUESTION:
{question}

AI RESPONSE:
{ai_response}

{ref_section}
REFERENCE CONTEXT (from knowledge base):
{context}

TASK:
Evaluate the factual accuracy of the AI response. Consider:
1. Are all stated facts, figures, dates, and names correct?
2. Do any claims contradict the reference answer or reference context?
3. Are there factual errors that could mislead a user?

Respond ONLY with valid JSON in this exact format:
{{
  "score": <number 0-10>,
  "reasoning": "<2-3 sentences explaining the score>",
  "incorrect_claims": ["<list specific incorrect claims if any>"]
}}"""

        raw = await self._call_llm(prompt)
        result = self._parse_json_response(raw)
        result["dimension"] = "accuracy"
        result.setdefault("score", 5.0)
        result.setdefault("reasoning", "Could not determine accuracy.")
        result.setdefault("incorrect_claims", [])
        return result
