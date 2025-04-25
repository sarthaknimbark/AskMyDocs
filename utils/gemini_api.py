import google.generativeai as genai
import time
import logging
from google.api_core.exceptions import DeadlineExceeded

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

    # Retry logic parameters
    initial_delay = 10.0  # Initial delay in seconds
    max_delay = 60.0      # Max retry delay in seconds
    retries = 5           # Number of retries
    delay_multiplier = 2  # Multiplier for increasing delay

    for attempt in range(retries):
        try:
            logger.debug(f"Attempt {attempt + 1}: Sending request with prompt: {prompt[:100]}...")  # Log part of the prompt
            response = model.generate_content(prompt)  # Make the API call
            logger.debug(f"Response received: {response.text[:100]}...")  # Log the response part
            return response.text.strip()
        
        except DeadlineExceeded as e:
            logger.error(f"Attempt {attempt + 1}: Timeout occurred while generating response. {e}")
            if attempt < retries - 1:
                # Wait before retrying
                wait_time = min(initial_delay * (delay_multiplier ** attempt), max_delay)
                logger.info(f"Retrying after {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                return "Sorry, the request timed out. Please try again later."
        
        except Exception as e:
            # Catch any other exceptions
            logger.error(f"Attempt {attempt + 1}: An unexpected error occurred: {e}")
            return "An error occurred. Please try again later."

    return "Maximum retry attempts reached. Please try again later."
