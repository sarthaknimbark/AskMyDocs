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
    st.set_page_config(page_title="AskMyDocs", page_icon="assets/logo.png", layout="wide")
    st.write(css, unsafe_allow_html=True)
    st.markdown(header, unsafe_allow_html=True)

    # Session state setup
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "processed" not in st.session_state:
        st.session_state.processed = False
    if "new_upload" not in st.session_state:
        st.session_state.new_upload = False

    # Sidebar for PDF upload
    with st.sidebar:
        st.header("📁 Upload your document here")
        pdf_docs = st.file_uploader("Upload PDFs", accept_multiple_files=True, type=["pdf"])

        if pdf_docs:
            if st.button("🔄 Process PDFs") and not st.session_state.new_upload:
                with st.spinner("Processing uploaded PDFs..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)

                    if vectorstore:
                        st.session_state.vectorstore = vectorstore
                        st.session_state.chat_history = []
                        st.session_state.processed = True
                        st.session_state.new_upload = True
                        st.success("✅ Documents processed successfully!")

    # Question input area
    if st.session_state.processed:
        st.subheader("💬 Ask your uploaded documents")

        user_question = st.text_input("Type your question")

        if st.button("Ask") and user_question:
            handle_userinput(user_question, st.session_state.vectorstore)

        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.session_state.new_upload = False
            st.session_state.processed = False
            st.success("Chat cleared!")
            st.rerun()

    else:
        st.info("Upload and process your PDFs to begin asking questions.", icon="ℹ️")

    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
