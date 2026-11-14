# M1.1 — Research & Technical Understanding

## 1. LLM Evaluation Techniques

### 1.1 Overview
LLM evaluation involves assessing the quality of model outputs across multiple dimensions. Evaluation can be:
- **Reference-based**: Compare against a ground-truth answer
- **Reference-free**: Evaluate without ground truth (e.g., using another LLM as judge)
- **Human-in-the-loop**: Human annotators score responses

### 1.2 Automated Evaluation Approaches

| Approach | Description | Pros | Cons |
|----------|-------------|------|------|
| **Exact Match (EM)** | Direct string comparison | Fast, deterministic | Rigid, misses paraphrases |
| **ROUGE / BLEU** | N-gram overlap metrics | Established, fast | Doesn't capture semantics |
| **BERTScore** | Contextual embedding similarity | Semantic awareness | Computationally heavier |
| **LLM-as-a-Judge** | Use an LLM to evaluate outputs | Flexible, nuanced | Potential bias, expensive |
| **RAG-grounded** | Retrieval + LLM evaluation | Factually grounded | Requires a knowledge base |

### 1.3 Key Evaluation Dimensions
- **Relevance**: Does the response address the question asked?
- **Factuality / Accuracy**: Are the stated facts correct?
- **Faithfulness**: Is the response consistent with retrieved sources?
- **Hallucination**: Does the response contain invented or unsupported claims?
- **Completeness**: Does the response cover all aspects of the question?

---

## 2. Hallucination Detection

### 2.1 Types of Hallucinations
1. **Intrinsic Hallucination**: Contradicts the provided context/source
2. **Extrinsic Hallucination**: Introduces information not in the source (may be true or false)
3. **Factual Hallucination**: States incorrect real-world facts

### 2.2 Detection Methods
- **NLI-based (Natural Language Inference)**: Check if the response entails or contradicts the source
- **Entity-level verification**: Verify named entities, dates, numbers against a knowledge base
- **Semantic similarity**: Measure embedding similarity between response and retrieved context
- **LLM-based verification**: Ask an LLM to check factual consistency
- **SelfCheckGPT**: Sample multiple responses; hallucinated facts tend to be inconsistent

### 2.3 Key Findings
- Hallucinations are more common in **open-domain QA** than in document-grounded settings
- Combining **retrieval (RAG)** with evaluation significantly improves factuality detection
- LLM-as-a-Judge with structured prompts achieves near-human inter-rater agreement on hallucination scoring

---

## 3. RAG Architecture

### 3.1 Core Components
```
Query → Embedding → Vector Search → Retrieved Chunks → LLM → Response
```

### 3.2 Retrieval Pipeline
1. **Document Ingestion**: Load raw documents/datasets
2. **Chunking**: Split into manageable segments (e.g., 512 tokens with 50-token overlap)
3. **Embedding**: Convert chunks to dense vectors (`all-MiniLM-L6-v2`, `text-embedding-004`)
4. **Indexing**: Store in a vector database (ChromaDB, FAISS, Pinecone)
5. **Retrieval**: Given a query, find top-k nearest neighbor chunks
6. **Augmentation**: Include retrieved chunks in LLM context for grounded evaluation

### 3.3 Chunking Strategies
| Strategy | Description | Best For |
|----------|-------------|----------|
| **Fixed-size** | Split by token count | Uniform documents |
| **Sentence-based** | Split at sentence boundaries | Preserves meaning |
| **Semantic** | Group semantically coherent sentences | High quality, slower |
| **Sliding window** | Overlapping chunks | Preserving context across boundaries |

**Chosen Strategy**: Sliding window with 512-char chunks and 50-char overlap — balances context preservation and retrieval precision.

---

## 4. LLM-as-a-Judge

### 4.1 Approach
Use a capable LLM (e.g., Gemini) to evaluate AI responses by:
- Providing the **question**, **AI response**, and optionally **reference answer** / **retrieved context**
- Asking the LLM to score along specific dimensions with a **structured prompt**
- Returning a **numerical score** (0–10) with **reasoning**

### 4.2 Scoring Prompt Design
Key elements of an effective judge prompt:
1. Clear role definition: "You are an expert evaluator..."
2. Explicit criteria per dimension
3. Chain-of-thought reasoning before final score
4. Structured output (JSON) for programmatic parsing

### 4.3 Bias Mitigation
- Use **calibrated prompts** with examples
- Apply **temperature=0** for deterministic evaluation
- Use **multiple runs** and average for critical evaluations
- Avoid **position bias** (don't always put reference answer first)

---

## 5. Evaluation Frameworks — RAGAS & TruLens

### 5.1 RAGAS
- **Purpose**: Evaluate RAG pipelines
- **Metrics**: Answer Relevancy, Faithfulness, Context Precision, Context Recall
- **Method**: LLM-based evaluation, reference-free for some metrics
- **Key Insight**: `Faithfulness = |supported claims| / |total claims in response|`

### 5.2 TruLens
- **Purpose**: Tracking and evaluating LLM applications
- **Features**: Feedback functions, tracing, dashboard UI
- **Metrics**: Groundedness, QA Relevance, Context Relevance (the "RAG Triad")
- **Key Insight**: The RAG Triad ensures end-to-end quality: relevant context → faithful answer → relevant to query

### 5.3 Design Decisions for Our System
| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Judge model | Gemini `gemini-3.8-flash` | Fast, capable, structured output |
| Retrieval | ChromaDB + `all-MiniLM-L6-v2` | Local, no external API for vectors |
| Scoring | 0–10 per dimension | Interpretable, granular |
| Output format | JSON with scores + reasoning | Machine-parseable + human-readable |
| Reference | Optional (reference-free capable) | Flexible deployment |

---

## 6. Public QA Benchmark Datasets

### 6.1 TruthfulQA
- **Purpose**: Measure truthfulness of LLM outputs
- **Size**: 817 questions across 38 categories
- **Format**: MC1 (single correct), MC2 (multiple correct), generation tasks
- **Key Property**: Questions are designed so that humans answering instinctively give incorrect answers
- **Categories**: Health, Law, Finance, Conspiracies, Misconceptions, etc.
- **HuggingFace**: `datasets.load_dataset("truthful_qa", "generation")`

### 6.2 SQuAD (Stanford Question Answering Dataset)
- **Purpose**: Reading comprehension — answer questions based on Wikipedia passages
- **Size**: SQuAD 1.1: 100K+ QA pairs; SQuAD 2.0: adds unanswerable questions
- **Format**: Context paragraph + question + answer span(s)
- **Key Property**: Provides reference answers with grounding context — ideal for faithfulness evaluation
- **HuggingFace**: `datasets.load_dataset("squad")`

### 6.3 Usage in Our System
| Dataset | Role |
|---------|------|
| TruthfulQA | Test hallucination detection; seed knowledge base with correct answers |
| SQuAD | RAG context chunks; test retrieval quality; reference answers for accuracy evaluation |

---

## 7. Technology Choices Summary

| Component | Choice | Alternatives Considered |
|-----------|--------|------------------------|
| Backend | FastAPI | Flask, Django |
| LLM | Google Gemini API | OpenAI GPT-4, Anthropic Claude |
| Embeddings | `all-MiniLM-L6-v2` | `text-embedding-004`, `ada-002` |
| Vector DB | ChromaDB | FAISS, Pinecone, Weaviate |
| Datasets | HuggingFace `datasets` | Manual download |
| Frontend | React + Vite + Tailwind | Streamlit, Gradio |
| DB | SQLite → PostgreSQL | MongoDB |
| Eval framework | Custom (RAGAS-inspired) | Direct RAGAS integration |

---

## 8. Implementation Strategy

1. **Build the knowledge base first** — seed with TruthfulQA + SQuAD, embed, index
2. **Build the input API** — accept submissions, validate, store
3. **Build judge agents** — one per dimension, structured prompts, Gemini backend
4. **Build orchestrator** — coordinate agents, aggregate scores
5. **Build evaluation pipeline** — RAG retrieval → agent evaluation → verdict
6. **Build results API + frontend** — display structured results

---
*Research conducted for Milestone 1.1 — Infosys Springboard Internship*
