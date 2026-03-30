# utils/langchain_utils.py
# Page-aware text splitter — chunks within each page so page metadata is never lost.
# Compatible with Python 3.14 (avoids spacy/pydantic v1 import chain).


def get_text_chunks(pages, chunk_size=1500, chunk_overlap=300):
    """Split page-aware text into overlapping chunks.

    Args:
        pages: list of dicts [{"page": int, "file": str, "text": str}, ...]
        chunk_size: max characters per chunk
        chunk_overlap: overlap between consecutive chunks

    Returns:
        list of strings, each prefixed with [Page X] for citation tracking.
    """
    if not pages:
        return []

    all_chunks = []

    for page_info in pages:
        page_num = page_info["page"]
        page_text = page_info["text"]
        file_name = page_info.get("file", "")

        if not page_text or not page_text.strip():
            continue

        # Split this single page into chunks
        page_chunks = _split_text(page_text, chunk_size, chunk_overlap)

        # Prepend page marker to every chunk from this page
        for chunk in page_chunks:
            prefix = f"[Page {page_num}]"
            if file_name:
                prefix = f"[{file_name} — Page {page_num}]"
            all_chunks.append(f"{prefix}\n{chunk}")

    return all_chunks


def _split_text(text, chunk_size, chunk_overlap):
    """Split text into overlapping chunks using recursive separators."""
    separators = ["\n\n", "\n", ". ", ", ", " "]
    return _recursive_split(text, separators, chunk_size, chunk_overlap)


def _recursive_split(text, separators, chunk_size, chunk_overlap):
    """Recursively split text using a hierarchy of separators."""
    # If text is already small enough, return it as-is
    if len(text) <= chunk_size:
        return [text.strip()] if text.strip() else []

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
