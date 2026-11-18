"""
Base Judge Agent — shared interface for all judge agents.
Each agent calls the Gemini API with a structured prompt and parses JSON output.
"""
import json
import re
from abc import ABC, abstractmethod
from typing import Optional

from google import genai
from core.config import settings


class BaseJudgeAgent(ABC):
    """
    Abstract base for all LLM-as-a-Judge evaluation agents.
    Uses Gemini API with structured JSON output.
    """

    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.llm_model

    def _build_system_prompt(self) -> str:
        return (
            "You are an expert AI evaluator. Your task is to evaluate AI-generated responses "
            "objectively and accurately. Always respond with valid JSON only. "
            "Do not include any text outside the JSON object. "
            "Use the exact field names specified in the prompt."
        )

    async def _call_llm(self, prompt: str) -> str:
        """Call Gemini API using generate_content with supported models."""
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-3.5-flash",
            "gemini-3.5-flash-lite",
        ]
        last_error = None
        for model_name in models_to_try:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={
                        "system_instruction": self._build_system_prompt(),
                        "temperature": 0.0,
                    },
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = e
                continue
        if last_error:
            raise last_error
        return ""

    def _parse_json_response(self, text: str) -> dict:
        """Extract and parse JSON from LLM response."""
        # Try direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        # Try extracting from markdown code block
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        # Fallback
        return {"error": "Could not parse response", "raw": text[:500]}

    @abstractmethod
    async def evaluate(self, **kwargs) -> dict:
        """Run evaluation and return a dict with score and reasoning."""
        ...
