"""
Verdict Agent — aggregates all dimension scores into a final weighted verdict.
Weights: Accuracy 30%, Hallucination 30%, Relevance 25%, Completeness 15%
"""

VERDICT_THRESHOLDS = [
    (9.0, "EXCELLENT"),
    (7.0, "GOOD"),
    (5.0, "ACCEPTABLE"),
    (3.0, "POOR"),
    (0.0, "DANGEROUS"),
]


class VerdictAgent:
    """
    Computes the weighted overall evaluation score and assigns a verdict label.
    Does not call the LLM — pure deterministic computation.
    """

    WEIGHTS = {
        "relevance": 0.25,
        "accuracy": 0.30,
        "hallucination": 0.30,
        "completeness": 0.15,
    }

    def compute_verdict(
        self,
        relevance: dict,
        accuracy: dict,
        hallucination: dict,
        completeness: dict,
    ) -> dict:
        """
        Compute weighted overall score and verdict label.

        Returns:
            dict with overall_score (float) and verdict (str)
        """
        scores = {
            "relevance": float(relevance.get("score", 5.0)),
            "accuracy": float(accuracy.get("score", 5.0)),
            "hallucination": float(hallucination.get("score", 5.0)),
            "completeness": float(completeness.get("score", 5.0)),
        }

        overall = sum(scores[dim] * self.WEIGHTS[dim] for dim in self.WEIGHTS)
        overall = round(overall, 2)

        verdict = "DANGEROUS"
        for threshold, label in VERDICT_THRESHOLDS:
            if overall >= threshold:
                verdict = label
                break

        return {
            "overall_score": overall,
            "verdict": verdict,
            "dimension_scores": scores,
            "weights_used": self.WEIGHTS,
        }
