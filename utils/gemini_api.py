import os
import time
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env so API key is available at import time
load_dotenv()

logger = logging.getLogger("gemini_logger")
logger.setLevel(logging.DEBUG)

# Lazy client — initialized on first use
_client = None


def _get_client():
    """Get or create the Gemini client (lazy init)."""
    global _client
    if _client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found. Please set it in your .env file."
            )
        _client = genai.Client(api_key=api_key)
    return _client


# System instruction — document-first with general knowledge fallback
SYSTEM_INSTRUCTION = """You are an expert document analyst and research assistant.
Your primary job is to answer questions based on the provided document context.

Follow these rules:

1. **Document-first**: Always prioritize the provided document context for your answer.
2. **Cite pages**: When your answer comes from the document, cite the source page, e.g., *(Page 3)*.
3. **General knowledge fallback**: If the document context does NOT contain the answer:
   - You may use your general knowledge to give a helpful answer.
   - Clearly indicate this by prefixing with: "📚 *Based on general knowledge (not found in your documents):*"
   - Keep the general knowledge answer concise and relevant.
4. **Structure your response** using Markdown for readability:
   - Use **bold** for key terms and important points
   - Use bullet points or numbered lists for multiple items
   - Use headings (##, ###) to organize long answers
   - Use tables when comparing data or listing structured info
   - Use > blockquotes for direct quotes from the document
5. Be thorough but concise — provide complete answers without unnecessary padding.
6. If the question is ambiguous, interpret it in the most helpful way based on the context available.
7. When multiple pages are relevant, synthesize information across all of them rather than only citing one page."""


def get_gemini_response(context, question, chat_history=None):
    """Generate an advanced response using Gemini with structured prompting.

    Args:
        context: Relevant document chunks from vector search
        question: User's question
        chat_history: Optional list of recent chat messages for multi-turn context
    """
    client = _get_client()

    # Build conversation-aware prompt
    history_section = ""
    if chat_history and len(chat_history) > 0:
        recent = chat_history[-6:]  # Last 3 Q&A pairs
        history_lines = []
        for msg in recent:
            role = "User" if msg["sender"] == "You" else "Assistant"
            history_lines.append(f"{role}: {msg['message'][:300]}")
        history_section = "\n\nRecent conversation:\n" + "\n".join(history_lines)

    prompt = f"""Document Context:
---
{context}
---
{history_section}

User Question: {question}

Provide a detailed, well-structured answer. Prioritize information from the document context above. If the answer is not found in the documents, use your general knowledge but clearly label it. Use Markdown formatting."""

    # Retry logic
    initial_delay = 5.0
    max_delay = 30.0
    retries = 3
    delay_multiplier = 2

    for attempt in range(retries):
        try:
            logger.debug(f"Attempt {attempt + 1}: Sending request...")
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.3,
                    max_output_tokens=4096,
                    top_p=0.9,
                ),
            )

            if response and response.text:
                logger.debug(f"Response received ({len(response.text)} chars)")
                return response.text.strip()
            else:
                logger.warning("Empty response received from Gemini")
                return "The model returned an empty response. Please try rephrasing your question."

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Attempt {attempt + 1}: Error — {error_msg}")

            if "deadline" in error_msg.lower() or "timeout" in error_msg.lower():
                if attempt < retries - 1:
                    wait_time = min(initial_delay * (delay_multiplier ** attempt), max_delay)
                    logger.info(f"Retrying after {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    return "The request timed out after multiple attempts. Please try again."

            return f"An error occurred: {error_msg}"

    return "Maximum retry attempts reached. Please try again later."
