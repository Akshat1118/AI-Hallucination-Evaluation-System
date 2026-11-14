"""
ChromaDB Vector Store — M1.4
Persistent vector store using ChromaDB for semantic retrieval.
"""
import chromadb
from chromadb.config import Settings
import uuid
import logging

logger = logging.getLogger(__name__)

COLLECTION_NAME = "eval_knowledge_base"


class ChromaVectorStore:
    """
    Wraps ChromaDB for storing and querying embedded knowledge base chunks.

    Supports:
    - add: Batch insert of chunks + embeddings + metadata
    - query: Semantic similarity search
    - count: Total indexed chunks
    """

    def __init__(self, persist_dir: str = "./knowledge_base/vectorstore/chroma_db"):
        self.persist_dir = persist_dir
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},  # Cosine similarity
        )
        logger.info(f"ChromaDB initialized at {persist_dir}. Collection: {COLLECTION_NAME}")

    def add(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ):
        """
        Add chunks to the vector store.

        Args:
            chunks: List of text chunks (documents)
            embeddings: Corresponding embedding vectors
            metadatas: Corresponding metadata dicts
        """
        ids = [str(uuid.uuid4()) for _ in chunks]
        # Clean metadata — ChromaDB requires string/int/float/bool values
        clean_meta = []
        for m in metadatas:
            clean_meta.append({k: str(v) if v is not None else "" for k, v in m.items()})

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=clean_meta,
        )
        logger.info(f"Added {len(chunks)} chunks to ChromaDB")

    def query(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """
        Semantic similarity search.

        Args:
            query_embedding: Query vector
            top_k: Number of results to return

        Returns:
            List of dicts with document, metadata, and distance score
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count() or 1),
            include=["documents", "metadatas", "distances"],
        )

        output = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]

        for doc, meta, dist in zip(docs, metas, dists):
            output.append({
                "document": doc,
                "metadata": meta,
                "similarity_score": round(1 - dist, 4),  # Convert distance to similarity
            })

        return output

    def count(self) -> int:
        """Return total number of indexed chunks."""
        return self.collection.count()

    def reset(self):
        """Clear all data from the collection (use with caution)."""
        self.client.delete_collection(COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        logger.warning("ChromaDB collection reset.")
