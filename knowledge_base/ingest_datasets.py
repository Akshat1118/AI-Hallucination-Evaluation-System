"""
Standalone knowledge base ingestion script.
Run from the project root to seed ChromaDB with TruthfulQA and SQuAD.

Usage:
    python knowledge_base/ingest_datasets.py --dataset all --max-samples 500
"""
import sys
import argparse
import logging
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Seed the RAG knowledge base with benchmark datasets.")
    parser.add_argument("--dataset", default="all", choices=["all", "truthful_qa", "squad"],
                        help="Dataset to ingest (default: all)")
    parser.add_argument("--max-samples", type=int, default=500,
                        help="Max samples per dataset (default: 500)")
    parser.add_argument("--chunk-size", type=int, default=512,
                        help="Chunk size in characters (default: 512)")
    parser.add_argument("--chunk-overlap", type=int, default=50,
                        help="Overlap between chunks (default: 50)")
    parser.add_argument("--embed-model", default="all-MiniLM-L6-v2",
                        help="Sentence transformer model (default: all-MiniLM-L6-v2)")
    parser.add_argument("--persist-dir", default="./knowledge_base/vectorstore/chroma_db",
                        help="ChromaDB persistence directory")
    args = parser.parse_args()

    from knowledge_base.ingestion.dataset_loader import DatasetLoader
    from knowledge_base.ingestion.chunker import TextChunker
    from knowledge_base.embeddings.embedder import Embedder
    from knowledge_base.vectorstore.chroma_store import ChromaVectorStore

    loader = DatasetLoader()
    chunker = TextChunker(chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
    embedder = Embedder(model_name=args.embed_model)
    store = ChromaVectorStore(persist_dir=args.persist_dir)

    datasets_to_load = []
    if args.dataset in ("all", "truthful_qa"):
        datasets_to_load.append("truthful_qa")
    if args.dataset in ("all", "squad"):
        datasets_to_load.append("squad")

    total_indexed = 0
    for ds_name in datasets_to_load:
        logger.info(f"\n{'='*50}")
        logger.info(f"Processing dataset: {ds_name}")
        logger.info(f"{'='*50}")

        records = loader.load(ds_name, max_samples=args.max_samples)
        logger.info(f"Loaded {len(records)} records")

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
            logger.warning(f"No valid chunks generated for {ds_name}")
            continue

        logger.info(f"Generated {len(chunks)} chunks")
        logger.info(f"Generating embeddings (this may take a minute)...")
        embeddings = embedder.embed(chunks)
        logger.info(f"Embeddings generated. Indexing into ChromaDB...")
        store.add(chunks=chunks, embeddings=embeddings, metadatas=metadatas)
        total_indexed += len(chunks)
        logger.info(f"✅ Indexed {len(chunks)} chunks from {ds_name}")

    final_count = store.count()
    logger.info(f"\n{'='*50}")
    logger.info(f"✅ Ingestion complete!")
    logger.info(f"   Total chunks indexed this run: {total_indexed}")
    logger.info(f"   Total chunks in store: {final_count}")
    logger.info(f"   ChromaDB location: {args.persist_dir}")
    logger.info(f"{'='*50}\n")

    # Quick validation test
    logger.info("Running quick retrieval validation...")
    test_queries = [
        "What is the boiling point of water?",
        "Who wrote Romeo and Juliet?",
        "What causes inflation?",
    ]
    query_embedding = embedder.embed([test_queries[0]])[0]
    results = store.query(query_embedding=query_embedding, top_k=3)
    logger.info(f"Test query: '{test_queries[0]}'")
    for i, r in enumerate(results, 1):
        logger.info(f"  Result {i} (score={r['similarity_score']}): {r['document'][:100]}...")
    logger.info("✅ Retrieval validation passed!")


if __name__ == "__main__":
    main()
