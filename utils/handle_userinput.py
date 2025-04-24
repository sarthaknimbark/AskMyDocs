import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from htmlTemplates.css import css
from htmlTemplates.header import header
from htmlTemplates.footer import footer
from htmlTemplates.bot_template import bot_template
from htmlTemplates.user_template import user_template
from utils.vectorstore import  search_docs
from utils.gemini_api import get_gemini_response

def handle_userinput(user_question, vectorstore):
    context = search_docs(vectorstore, user_question)
    response_text = get_gemini_response(context, user_question)

    # Add chat history as sender/message instead of role/content
    st.session_state.chat_history.append({"sender": "You", "message": user_question})
    st.session_state.chat_history.append({"sender": "AskMyDocs", "message": response_text})

    # Display chat history
    for msg in st.session_state.chat_history:
        sender = msg["sender"]
        message = msg["message"]
        if sender == "You":
            st.write(user_template.replace("{{MSG}}", message), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message), unsafe_allow_html=True)
