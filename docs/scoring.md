# Evaluation Scoring Dimensions & Methodology

## Scoring Scale
All dimensions are scored from **0 to 10**:
- **0–3**: Poor (significant issues)
- **4–6**: Moderate (some issues)
- **7–8**: Good (minor issues)
- **9–10**: Excellent (no significant issues)

---

## Dimension Definitions

### 1. Relevance (0–10)
**Definition**: How well does the AI response address the actual question asked?

| Score | Description |
|-------|-------------|
| 9–10 | Directly and fully addresses the question |
| 7–8 | Mostly relevant with minor off-topic content |
| 4–6 | Partially relevant; misses key aspects |
| 1–3 | Mostly irrelevant to the question |
| 0 | Completely off-topic |

**Judge Prompt Focus**: Compare question intent vs. response content; check for topic drift.

---

### 2. Accuracy (0–10)
**Definition**: Are the factual claims in the response verifiable and correct?

| Score | Description |
|-------|-------------|
| 9–10 | All verifiable facts are correct |
| 7–8 | Mostly accurate; 1–2 minor inaccuracies |
| 4–6 | Some correct facts but notable inaccuracies |
| 1–3 | Many factual errors |
| 0 | Entirely inaccurate |

**Judge Prompt Focus**: Cross-reference with retrieved knowledge base context and reference answer.

---

### 3. Hallucination Score (0–10)
**Definition**: Does the response contain fabricated, invented, or unsupported information?  
*(Higher score = LESS hallucination = BETTER)*

| Score | Description |
|-------|-------------|
| 9–10 | No hallucinated content; all claims grounded |
| 7–8 | Minimal hallucination; claims mostly supported |
| 4–6 | Moderate hallucination; some unsupported claims |
| 1–3 | Heavy hallucination; majority unsupported |
| 0 | Completely fabricated |

**Hallucination Severity Labels**:
- `NONE`: Score 9–10
- `MINOR`: Score 7–8  
- `MODERATE`: Score 4–6  
- `SEVERE`: Score 1–3
- `CRITICAL`: Score 0

**Judge Prompt Focus**: Identify claims not supported by context or reference; flag specific hallucinated segments.

---

### 4. Completeness (0–10)
**Definition**: Does the response cover all relevant aspects of the question?

| Score | Description |
|-------|-------------|
| 9–10 | Fully comprehensive; nothing important omitted |
| 7–8 | Covers main points; minor aspects missing |
| 4–6 | Covers some aspects; significant gaps |
| 1–3 | Very incomplete; most of the answer is missing |
| 0 | Does not answer the question at all |

**Judge Prompt Focus**: Identify key expected topics for the question; check coverage vs. reference answer.

---

## Overall Verdict Calculation

### Weighted Score Formula

```
Overall = (Relevance × 0.25) + (Accuracy × 0.30) + (Hallucination × 0.30) + (Completeness × 0.15)
```

**Rationale for weights**:
- Accuracy + Hallucination = 60% → Factual correctness is the primary concern
- Relevance = 25% → Response must be on-topic
- Completeness = 15% → Completeness matters but partial answers still have value

### Verdict Labels

| Overall Score | Verdict Label | Recommendation |
|---------------|---------------|----------------|
| 9.0–10.0 | ✅ EXCELLENT | Safe to use |
| 7.0–8.9 | ✅ GOOD | Minor review recommended |
| 5.0–6.9 | ⚠️ ACCEPTABLE | Use with caution |
| 3.0–4.9 | ❌ POOR | Do not use without revision |
| 0.0–2.9 | 🚫 DANGEROUS | Do not use; highly misleading |

---

## Evaluation Output Format

```json
{
  "evaluation_id": "uuid",
  "question": "...",
  "ai_response": "...",
  "scores": {
    "relevance": {
      "score": 8.5,
      "reasoning": "The response directly addresses..."
    },
    "accuracy": {
      "score": 7.0,
      "reasoning": "Most facts are correct, however..."
    },
    "hallucination": {
      "score": 6.5,
      "severity": "MODERATE",
      "reasoning": "The response contains unsupported claims about...",
      "hallucinated_segments": ["..."]
    },
    "completeness": {
      "score": 9.0,
      "reasoning": "The response covers all key aspects..."
    }
  },
  "overall_score": 7.4,
  "verdict": "GOOD",
  "retrieved_context": ["..."],
  "created_at": "2026-11-15T03:00:00Z"
}
```
