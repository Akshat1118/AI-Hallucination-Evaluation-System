"""
Embedding Generator — M1.4
Uses sentence-transformers to embed text chunks for vector store indexing.
Default model: all-MiniLM-L6-v2 (fast, 384-dim, good quality for semantic similarity)
"""
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

logger = logging.getLogger(__name__)


class Embedder:
    """
    Generates dense vector embeddings using sentence-transformers.

    Model choices:
    - all-MiniLM-L6-v2: 384-dim, fast, good quality (default)
    - all-mpnet-base-v2: 768-dim, higher quality, slower
    - multi-qa-MiniLM-L6-cos-v1: optimized for semantic search / QA
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(f"Embedding model loaded. Dimension: {self.embedding_dim}")

    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (each is a list of floats)
        """
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=len(texts) > 100,
            convert_to_numpy=True,
            normalize_embeddings=True,  # L2-normalize for cosine similarity
        )

        return embeddings.tolist()

    def embed_single(self, text: str) -> list[float]:
        """Embed a single text string."""
        return self.embed([text])[0]
