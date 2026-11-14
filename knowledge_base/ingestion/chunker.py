"""
Text Chunker — M1.4
Splits long documents into overlapping chunks for vector store indexing.
Strategy: Sliding window (fixed-size with overlap), respecting sentence boundaries.
"""
import re


class TextChunker:
    """
    Splits text into overlapping chunks for embedding and retrieval.

    Parameters:
        chunk_size (int): Target character length per chunk (default 512)
        chunk_overlap (int): Characters to overlap between chunks (default 50)
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> list[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: Input text to split

        Returns:
            List of text chunks
        """
        if not text or not text.strip():
            return []

        # Clean text
        text = self._clean(text)

        # If short enough, return as-is
        if len(text) <= self.chunk_size:
            return [text]

        # Split into sentences first for cleaner boundaries
        sentences = self._split_sentences(text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # If adding this sentence would exceed chunk_size, save current chunk
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                # Start new chunk with overlap from end of previous chunk
                overlap_text = current_chunk[-self.chunk_overlap:] if self.chunk_overlap else ""
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += (" " if current_chunk else "") + sentence

        # Add remaining chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return [c for c in chunks if len(c) > 20]  # Filter out very short chunks

    def _clean(self, text: str) -> str:
        """Remove excessive whitespace and normalize text."""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences."""
        # Simple sentence splitter using common terminators
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
