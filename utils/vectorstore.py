from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st


def get_vectorstore(text_chunks):
    """Create a FAISS vector store from text chunks using HuggingFace embeddings."""
    if not text_chunks:
        st.error("No text chunks to process.")
        return None

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)


def search_docs(vectorstore, query, k=8):
    """Search the vector store for relevant document chunks.

    Returns top-k chunks with relevance scores. Uses similarity_search_with_score
    to enable score-based filtering of low-relevance results.
    Retrieves k=8 chunks (up from 5) for broader document coverage.
    Threshold relaxed to 2.0 (from 1.5) to include more marginally relevant content.
    """
    results = vectorstore.similarity_search_with_score(query, k=k)

    # Filter out low-relevance chunks (higher score = less relevant in FAISS L2)
    filtered = [(doc, score) for doc, score in results if score < 2.0]

    if not filtered:
        # If all filtered out, return at least top 2 results
        filtered = results[:2]

    return "\n\n---\n\n".join(doc.page_content for doc, _ in filtered)