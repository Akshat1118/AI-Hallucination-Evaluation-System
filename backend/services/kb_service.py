"""
Knowledge Base Service — M1.4
Handles dataset ingestion, chunking, embedding, and ChromaDB vector store operations.
Datasets: TruthfulQA and SQuAD from Hugging Face
"""
from typing import Optional
import asyncio
import logging

logger = logging.getLogger(__name__)


class KnowledgeBaseService:
    """
    Manages the reference knowledge base:
    - Load TruthfulQA and SQuAD from Hugging Face
    - Chunk, embed, and index into ChromaDB
    - Retrieve relevant context via semantic search
    """

    @staticmethod
    async def ingest(dataset: str = "all", max_samples: int = 500):
        """Trigger ingestion in a thread pool to avoid blocking the event loop."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, KnowledgeBaseService._ingest_sync, dataset, max_samples
        )

    @staticmethod
    def _ingest_sync(dataset: str = "all", max_samples: int = 500):
        """Synchronous ingestion — called from thread pool."""
        from knowledge_base.ingestion.dataset_loader import DatasetLoader
        from knowledge_base.ingestion.chunker import TextChunker
        from knowledge_base.embeddings.embedder import Embedder
        from knowledge_base.vectorstore.chroma_store import ChromaVectorStore
        from core.config import settings

        loader = DatasetLoader()
        chunker = TextChunker(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        embedder = Embedder(model_name=settings.embed_model)
        store = ChromaVectorStore(persist_dir=settings.chroma_persist_dir)

        datasets_to_load = []
        if dataset in ("all", "truthful_qa"):
            datasets_to_load.append("truthful_qa")
        if dataset in ("all", "squad"):
            datasets_to_load.append("squad")

        for ds_name in datasets_to_load:
            logger.info(f"Loading dataset: {ds_name}")
            records = loader.load(ds_name, max_samples=max_samples)
            logger.info(f"Loaded {len(records)} records from {ds_name}")

            chunks = []
            metadatas = []
            for record in records:
                text = record.get("context") or record.get("answer") or ""
                if not text.strip():
                    continue
                for chunk in chunker.chunk(text):
                    chunks.append(chunk)
                    metadatas.append({
                        "dataset": ds_name,
                        "question": record.get("question", "")[:200],
                        "answer": record.get("answer", "")[:500],
                        "source": record.get("source", ds_name),
                    })

            if not chunks:
                logger.warning(f"No chunks generated for {ds_name}")
                continue

            logger.info(f"Embedding {len(chunks)} chunks from {ds_name}...")
            embeddings = embedder.embed(chunks)
            store.add(chunks=chunks, embeddings=embeddings, metadatas=metadatas)
            logger.info(f"Indexed {len(chunks)} chunks from {ds_name} into ChromaDB")

    @staticmethod
    async def retrieve(query: str, top_k: int = 5) -> list[dict]:
        """Retrieve relevant context chunks for a query."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, KnowledgeBaseService._retrieve_sync, query, top_k
        )

    @staticmethod
    def _retrieve_sync(query: str, top_k: int = 5) -> list[dict]:
        from knowledge_base.embeddings.embedder import Embedder
        from knowledge_base.vectorstore.chroma_store import ChromaVectorStore
        from core.config import settings

        embedder = Embedder(model_name=settings.embed_model)
        store = ChromaVectorStore(persist_dir=settings.chroma_persist_dir)

        query_embedding = embedder.embed([query])[0]
        results = store.query(query_embedding=query_embedding, top_k=top_k)
        return results

    @staticmethod
    async def get_stats() -> dict:
        """Get knowledge base statistics."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, KnowledgeBaseService._stats_sync)

    @staticmethod
    def _stats_sync() -> dict:
        from knowledge_base.vectorstore.chroma_store import ChromaVectorStore
        from core.config import settings

        try:
            store = ChromaVectorStore(persist_dir=settings.chroma_persist_dir)
            count = store.count()
            return {"total_indexed_chunks": count, "status": "ready"}
        except Exception as e:
            return {"total_indexed_chunks": 0, "status": "empty", "error": str(e)}
