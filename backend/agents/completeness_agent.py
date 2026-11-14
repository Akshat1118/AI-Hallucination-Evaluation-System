"""Completeness Judge Agent — evaluates if the response fully answers the question."""
from typing import Optional
from agents.base_agent import BaseJudgeAgent


class CompletenessJudgeAgent(BaseJudgeAgent):
    """
    Evaluates how completely the AI response addresses the question.
    Score: 0–10 (10 = fully complete)
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

        prompt = f"""You are evaluating the COMPLETENESS of an AI response.

QUESTION:
{question}

AI RESPONSE:
{ai_response}

{ref_section}
REFERENCE CONTEXT (from knowledge base):
{context}

TASK:
Evaluate how completely the AI response answers the question. Consider:
1. Does it cover all key aspects expected for this type of question?
2. Are there important omissions that would leave the user without a full answer?
3. If a reference answer is provided, what important content is missing?

Respond ONLY with valid JSON in this exact format:
{{
  "score": <number 0-10>,
  "reasoning": "<2-3 sentences explaining the score>",
  "missing_aspects": ["<list key topics or information that is missing>"]
}}"""

        raw = await self._call_llm(prompt)
        result = self._parse_json_response(raw)
        result["dimension"] = "completeness"
        result.setdefault("score", 5.0)
        result.setdefault("reasoning", "Could not determine completeness.")
        result.setdefault("missing_aspects", [])
        return result
