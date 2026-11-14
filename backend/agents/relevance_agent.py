"""Relevance Judge Agent — evaluates how relevant the response is to the question."""
from agents.base_agent import BaseJudgeAgent


class RelevanceJudgeAgent(BaseJudgeAgent):
    """
    Evaluates the relevance of an AI response to the question asked.
    Score: 0–10 (10 = perfectly relevant)
    """

    async def evaluate(self, question: str, ai_response: str, context: str = "") -> dict:
        prompt = f"""You are evaluating the RELEVANCE of an AI response to a question.

QUESTION:
{question}

AI RESPONSE:
{ai_response}

REFERENCE CONTEXT (from knowledge base):
{context}

TASK:
Evaluate how relevant the AI response is to the question. Consider:
1. Does the response directly address what was asked?
2. Is the response on-topic without unnecessary tangents?
3. Does it answer the specific type of question asked (factual, explanatory, etc.)?

Respond ONLY with valid JSON in this exact format:
{{
  "score": <number 0-10>,
  "reasoning": "<2-3 sentences explaining the score>",
  "issues": ["<list any specific relevance issues>"]
}}"""

        raw = await self._call_llm(prompt)
        result = self._parse_json_response(raw)
        result["dimension"] = "relevance"
        result.setdefault("score", 5.0)
        result.setdefault("reasoning", "Could not determine relevance.")
        result.setdefault("issues", [])
        return result
