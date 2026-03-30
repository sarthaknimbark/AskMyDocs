import os
from dotenv import load_dotenv
import streamlit as st

from htmlTemplates.css import css
from htmlTemplates.header import header
from htmlTemplates.footer import footer

from utils.pdf_processing import get_pdf_text
from utils.langchain_utils import get_text_chunks
from utils.vectorstore import get_vectorstore
from utils.handle_userinput import handle_userinput


def main():
    # Load environment variables
    load_dotenv()

    # Streamlit page setup
    st.set_page_config(
        page_title="AskMyDocs",
        page_icon="assets/logo.png",
        layout="wide",
    )
    st.write(css, unsafe_allow_html=True)
    st.markdown(header, unsafe_allow_html=True)

    # ── API Key Validation ──────────────────────────────────
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key.strip() == "":
        st.error(
            "🔑 **Google API Key not found!**\n\n"
            "Please add your API key to the `.env` file:\n"
            "```\nGOOGLE_API_KEY=your_key_here\n```\n"
            "Get one free at [Google AI Studio](https://aistudio.google.com/apikey)."
        )
        st.stop()

    # ── Session State Setup ─────────────────────────────────
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "processed" not in st.session_state:
        st.session_state.processed = False
    if "doc_stats" not in st.session_state:
        st.session_state.doc_stats = {}

    # ── Sidebar ─────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 📁 Upload Documents")
        st.caption("Upload one or more PDF files to get started.")

        pdf_docs = st.file_uploader(
            "Choose PDF files",
            accept_multiple_files=True,
            type=["pdf"],
            label_visibility="collapsed",
        )

        if pdf_docs:
            if st.button("⚡ Process PDFs", use_container_width=True):
                with st.spinner("Extracting text & building index..."):
                    # Extract text with page tracking
                    pages, page_count = get_pdf_text(pdf_docs)

                    if not pages:
                        st.error("❌ No text could be extracted from the uploaded PDFs.")
                    else:
                        # Chunk and index (page-aware)
                        text_chunks = get_text_chunks(pages)
                        vectorstore = get_vectorstore(text_chunks)

                        if vectorstore:
                            st.session_state.vectorstore = vectorstore
                            st.session_state.chat_history = []
                            st.session_state.processed = True
                            st.session_state.doc_stats = {
                                "files": len(pdf_docs),
                                "pages": page_count,
                                "chunks": len(text_chunks),
                            }
                            st.success("✅ Documents processed successfully!")

        # Show document stats
        if st.session_state.processed and st.session_state.doc_stats:
            stats = st.session_state.doc_stats
            st.markdown("---")
            st.markdown("#### 📊 Document Stats")
            col1, col2, col3 = st.columns(3)
            col1.metric("Files", stats.get("files", 0))
            col2.metric("Pages", stats.get("pages", 0))
            col3.metric("Chunks", stats.get("chunks", 0))

        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.processed = False
            st.session_state.vectorstore = None
            st.session_state.doc_stats = {}
            st.rerun()

    # ── Main Chat Area ──────────────────────────────────────
    if st.session_state.processed:
        st.markdown("### 💬 Ask your documents anything")

        user_question = st.text_input(
            "Type your question here...",
            placeholder="e.g. What are the key findings in section 3?",
            label_visibility="collapsed",
        )

        if st.button("🚀 Ask", use_container_width=False) and user_question:
            with st.spinner("🔎 Searching documents & generating response..."):
                handle_userinput(user_question, st.session_state.vectorstore)

    else:
        st.markdown(
            """
            <div style="text-align:center; padding: 3rem 1rem; opacity: 0.6;">
                <p style="font-size: 3rem; margin-bottom: 0.5rem;">📄</p>
                <p style="font-size: 1.1rem;">Upload and process your PDFs from the sidebar to begin asking questions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(footer, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
