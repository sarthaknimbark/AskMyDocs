import re
import streamlit as st
from PyPDF2 import PdfReader


def get_pdf_text(pdf_docs):
    """Extract text from uploaded PDF files with page number tracking.

    Returns a tuple: (pages_list, total_page_count)
    where pages_list is a list of dicts: [{"page": 1, "text": "..."}, ...]
    Each page's text is cleaned and stored separately so downstream
    chunking can split within pages without losing page metadata.
    """
    pages = []
    total_pages = 0

    for pdf in pdf_docs:
        try:
            reader = PdfReader(pdf)
            pdf_name = getattr(pdf, "name", "unknown")
            for i, page in enumerate(reader.pages, start=1):
                total_pages += 1
                page_text = page.extract_text()
                if page_text:
                    # Clean up garbled whitespace
                    page_text = re.sub(r"[ \t]+", " ", page_text)
                    page_text = re.sub(r"\n{3,}", "\n\n", page_text)
                    pages.append({
                        "page": total_pages,
                        "file": pdf_name,
                        "text": page_text.strip(),
                    })
        except Exception as e:
            st.error(f"Error reading PDF '{getattr(pdf, 'name', 'unknown')}': {e}")

    return pages, total_pages