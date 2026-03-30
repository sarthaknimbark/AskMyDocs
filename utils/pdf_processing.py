import re
import streamlit as st
from PyPDF2 import PdfReader


def get_pdf_text(pdf_docs):
    """Extract text from uploaded PDF files with page number tracking.
    
    Each page's text is prefixed with [Page X] so downstream chunks
    and the LLM can cite sources back to specific pages.
    Returns a tuple: (full_text, total_page_count)
    """
    text = ""
    total_pages = 0

    for pdf in pdf_docs:
        try:
            reader = PdfReader(pdf)
            for i, page in enumerate(reader.pages, start=1):
                total_pages += 1
                page_text = page.extract_text()
                if page_text:
                    # Clean up garbled whitespace
                    page_text = re.sub(r"[ \t]+", " ", page_text)
                    page_text = re.sub(r"\n{3,}", "\n\n", page_text)
                    text += f"\n\n[Page {total_pages}]\n{page_text.strip()}"
        except Exception as e:
            st.error(f"❌ Error reading PDF '{getattr(pdf, 'name', 'unknown')}': {e}")

    return text.strip(), total_pages