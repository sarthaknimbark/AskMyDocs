import streamlit as st
from htmlTemplates.bot_template import bot_template
from htmlTemplates.user_template import user_template
from utils.vectorstore import search_docs
from utils.gemini_api import get_gemini_response


def handle_userinput(user_question, vectorstore):
    """Handle user question: search docs, get AI response, render chat."""
    # Search for relevant context
    context = search_docs(vectorstore, user_question)

    # Pass chat history for multi-turn awareness
    response_text = get_gemini_response(
        context,
        user_question,
        chat_history=st.session_state.get("chat_history", []),
    )

    # Append to chat history
    st.session_state.chat_history.append(
        {"sender": "You", "message": user_question}
    )
    st.session_state.chat_history.append(
        {"sender": "AskMyDocs", "message": response_text}
    )

    # Display full chat history
    for msg in st.session_state.chat_history:
        sender = msg["sender"]
        message = msg["message"]
        if sender == "You":
            st.write(
                user_template.replace("{{MSG}}", message),
                unsafe_allow_html=True,
            )
        else:
            # Render bot response with Markdown support
            st.write(
                bot_template.replace("{{MSG}}", ""),
                unsafe_allow_html=True,
            )
            st.markdown(message)
