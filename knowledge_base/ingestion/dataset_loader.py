"""
Dataset Loader — M1.4
Loads TruthfulQA and SQuAD from Hugging Face datasets library.
Standardizes records into a uniform format.
"""
from datasets import load_dataset
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DatasetLoader:
    """
    Loads and standardizes public QA benchmark datasets.

    Supported datasets:
    - TruthfulQA (generation split)
    - SQuAD (train split)

    All records are normalized to:
    {
        "question": str,
        "answer": str,
        "context": str,
        "source": str,
    }
    """

    def load(self, dataset_name: str, max_samples: int = 500) -> list[dict]:
        """
        Load and return normalized records.

        Args:
            dataset_name: "truthful_qa" or "squad"
            max_samples: Maximum number of records to load

        Returns:
            List of normalized record dicts
        """
        if dataset_name == "truthful_qa":
            return self._load_truthful_qa(max_samples)
        elif dataset_name == "squad":
            return self._load_squad(max_samples)
        else:
            raise ValueError(f"Unsupported dataset: {dataset_name}. Use 'truthful_qa' or 'squad'.")

    def _load_truthful_qa(self, max_samples: int) -> list[dict]:
        """Load TruthfulQA generation split."""
        logger.info("Loading TruthfulQA from Hugging Face...")
        try:
            ds = load_dataset("truthful_qa", "generation", split="validation")
        except Exception as e:
            logger.error(f"Failed to load TruthfulQA: {e}")
            return []

        records = []
        for item in ds.select(range(min(max_samples, len(ds)))):
            # TruthfulQA has 'best_answer' and 'correct_answers'
            best_answer = item.get("best_answer", "")
            correct_answers = item.get("correct_answers", [])
            all_answers = [best_answer] + correct_answers
            combined_answer = " | ".join(a for a in all_answers if a)

            records.append({
                "question": item.get("question", ""),
                "answer": best_answer,
                "context": combined_answer,
                "source": "truthful_qa",
                "category": item.get("category", ""),
            })

        logger.info(f"Loaded {len(records)} records from TruthfulQA")
        return records

    def _load_squad(self, max_samples: int) -> list[dict]:
        """Load SQuAD 1.1 training split."""
        logger.info("Loading SQuAD from Hugging Face...")
        try:
            ds = load_dataset("squad", split="train")
        except Exception as e:
            logger.error(f"Failed to load SQuAD: {e}")
            return []

        records = []
        for item in ds.select(range(min(max_samples, len(ds)))):
            # SQuAD has 'context', 'question', and 'answers' (list of answer spans)
            answers = item.get("answers", {})
            answer_texts = answers.get("text", [])
            best_answer = answer_texts[0] if answer_texts else ""

            records.append({
                "question": item.get("question", ""),
                "answer": best_answer,
                "context": item.get("context", ""),
                "source": "squad",
                "title": item.get("title", ""),
            })

        logger.info(f"Loaded {len(records)} records from SQuAD")
        return records
