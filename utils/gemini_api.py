import google.generativeai as genai
from google.api_core.retry import Retry
from google.api_core.exceptions import DeadlineExceeded
from google.api_core.timeout import ExponentialTimeout
import logging

def get_gemini_response(context, question):
    # Set up logger for debugging
    logger = logging.getLogger("gemini_logger")
    logger.setLevel(logging.DEBUG)
    
    # Initialize the GenerativeModel
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    
    # Prepare the prompt with the provided context and question
    prompt = f"""Use the following context to answer the question below.

Context:
{context}

Question: {question}
Answer:"""

    # Define retry strategy
    retry_strategy = Retry(
        initial=10.0,  # Initial retry delay (seconds)
        maximum=120.0,  # Maximum retry delay (seconds)
        multiplier=2.0,  # Multiplier for increasing retry delay
        deadline=600.0  # Total time to retry before giving up (seconds)
    )
    
    try:
        logger.debug(f"Attempting to generate content with prompt: {prompt[:100]}...")  # Log part of the prompt
        response = model.generate_content(prompt, retry=retry_strategy)
        logger.debug(f"Response received: {response.text[:100]}...")  # Log the response part
        return response.text.strip()
    except DeadlineExceeded as e:
        # Log the timeout error
        logger.error(f"Error: Timeout occurred while generating response. {e}")
        return "Sorry, the request timed out. Please try again later."
    except Exception as e:
        # Log any other error
        logger.error(f"Error: An unexpected error occurred: {e}")
        return "An error occurred. Please try again later."
