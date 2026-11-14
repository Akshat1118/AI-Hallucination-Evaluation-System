"""
Unit tests for Milestone 1 components.
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestTextChunker:
    """Test M1.4 — Text Chunker"""

    def test_short_text_returned_as_single_chunk(self):
        from knowledge_base.ingestion.chunker import TextChunker
        chunker = TextChunker(chunk_size=512, chunk_overlap=50)
        text = "This is a short text."
        chunks = chunker.chunk(text)
        assert len(chunks) == 1
        assert chunks[0] == "This is a short text."

    def test_long_text_splits_into_multiple_chunks(self):
        from knowledge_base.ingestion.chunker import TextChunker
        chunker = TextChunker(chunk_size=100, chunk_overlap=20)
        text = " ".join(["This is a sentence."] * 20)
        chunks = chunker.chunk(text)
        assert len(chunks) > 1

    def test_empty_text_returns_empty(self):
        from knowledge_base.ingestion.chunker import TextChunker
        chunker = TextChunker()
        assert chunker.chunk("") == []
        assert chunker.chunk("   ") == []


class TestVerdictAgent:
    """Test M1.2 — Verdict computation"""

    def test_excellent_verdict(self):
        from backend.agents.verdict_agent import VerdictAgent
        agent = VerdictAgent()
        result = agent.compute_verdict(
            relevance={"score": 10.0},
            accuracy={"score": 10.0},
            hallucination={"score": 10.0},
            completeness={"score": 10.0},
        )
        assert result["overall_score"] == 10.0
        assert result["verdict"] == "EXCELLENT"

    def test_dangerous_verdict(self):
        from backend.agents.verdict_agent import VerdictAgent
        agent = VerdictAgent()
        result = agent.compute_verdict(
            relevance={"score": 0.0},
            accuracy={"score": 0.0},
            hallucination={"score": 0.0},
            completeness={"score": 0.0},
        )
        assert result["overall_score"] == 0.0
        assert result["verdict"] == "DANGEROUS"

    def test_weighted_calculation(self):
        from backend.agents.verdict_agent import VerdictAgent
        agent = VerdictAgent()
        result = agent.compute_verdict(
            relevance={"score": 8.0},
            accuracy={"score": 7.0},
            hallucination={"score": 6.0},
            completeness={"score": 9.0},
        )
        expected = 8.0 * 0.25 + 7.0 * 0.30 + 6.0 * 0.30 + 9.0 * 0.15
        assert abs(result["overall_score"] - expected) < 0.01


class TestEvaluationInput:
    """Test M1.3 — Input validation schemas"""

    def test_valid_input(self):
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
        from api.routes.evaluation import EvaluationRequest
        req = EvaluationRequest(
            question="What is the capital of France?",
            ai_response="The capital of France is Paris.",
        )
        assert req.question == "What is the capital of France?"
        assert req.ai_response == "The capital of France is Paris."

    def test_whitespace_stripped(self):
        from api.routes.evaluation import EvaluationRequest
        req = EvaluationRequest(
            question="  What is 2 + 2?  ",
            ai_response="  It is 4.  ",
        )
        assert req.question == "What is 2 + 2?"
        assert req.ai_response == "It is 4."

    def test_blank_question_raises_error(self):
        from pydantic import ValidationError
        from api.routes.evaluation import EvaluationRequest
        with pytest.raises(ValidationError):
            EvaluationRequest(question="   ", ai_response="Some answer")
