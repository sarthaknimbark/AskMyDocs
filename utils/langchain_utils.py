# utils/langchain_utils.py
# Custom text splitter to avoid langchain_text_splitters import
# which triggers spacy -> pydantic v1 crash on Python 3.14


def get_text_chunks(text, chunk_size=1000, chunk_overlap=200):
    """Split text into overlapping chunks using recursive splitting.

    Uses paragraph -> sentence -> word boundaries for better
    semantic coherence. Compatible with Python 3.14 (avoids
    the spacy/pydantic v1 import chain).
    """
    if not text or not text.strip():
        return []

    separators = ["\n\n", "\n", ". ", " "]
    return _recursive_split(text, separators, chunk_size, chunk_overlap)


def _recursive_split(text, separators, chunk_size, chunk_overlap):
    """Recursively split text using a hierarchy of separators."""
    final_chunks = []
    separator = separators[-1]  # default: split by space

    # Find the best separator that actually exists in the text
    for sep in separators:
        if sep in text:
            separator = sep
            break

    # Split with chosen separator
    splits = text.split(separator)

    current_chunk = []
    current_length = 0

    for piece in splits:
        piece_len = len(piece) + len(separator)

        if current_length + piece_len > chunk_size and current_chunk:
            # Save current chunk
            chunk_text = separator.join(current_chunk).strip()
            if chunk_text:
                final_chunks.append(chunk_text)

            # Calculate overlap: keep trailing pieces that fit in overlap window
            overlap_chunks = []
            overlap_len = 0
            for prev_piece in reversed(current_chunk):
                if overlap_len + len(prev_piece) + len(separator) <= chunk_overlap:
                    overlap_chunks.insert(0, prev_piece)
                    overlap_len += len(prev_piece) + len(separator)
                else:
                    break

            current_chunk = overlap_chunks
            current_length = overlap_len

        current_chunk.append(piece)
        current_length += piece_len

    # Don't forget the last chunk
    if current_chunk:
        chunk_text = separator.join(current_chunk).strip()
        if chunk_text:
            final_chunks.append(chunk_text)

    return final_chunks
