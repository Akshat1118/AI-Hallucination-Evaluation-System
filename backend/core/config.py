"""
Core configuration management using pydantic-settings.
Reads from environment variables or .env file.
"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Gemini API
    gemini_api_key: str = ""
    llm_model: str = "gemini-3.8-flash"

    # Database
    database_url: str = "sqlite+aiosqlite:///./hallucination_eval.db"

    # ChromaDB
    chroma_persist_dir: str = "./knowledge_base/vectorstore/chroma_db"
    chroma_collection_name: str = "eval_knowledge_base"

    # Embedding
    embed_model: str = "all-MiniLM-L6-v2"

    # RAG settings
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k_retrieval: int = 5

    # App settings
    debug: bool = True
    app_title: str = "AI Hallucination Evaluation System"
    app_version: str = "1.0.0"

    model_config = {"env_file": "../.env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
