import google.generativeai as genai
from google.api_core.retry import Retry
from google.api_core.exceptions import DeadlineExceeded
from google.api_core.timeout import ExponentialTimeout
import time

def get_gemini_response(context, question):
    # Initialize the GenerativeModel
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    
    # Prepare the prompt with the provided context and question
    prompt = f"""Use the following context to answer the question below.

Context:
{context}

Question: {question}
Answer:"""
    
    # Define a retry strategy in case of timeout or failure
    retry_strategy = Retry(
        initial=10.0,  # Initial retry delay (seconds)
        maximum=60.0,  # Maximum retry delay (seconds)
        multiplier=1.5,  # Multiplier for increasing retry delay
        deadline=180.0  # Total time to retry before giving up (seconds)
    )
    
    try:
        # Attempt to generate content with retries
        response = model.generate_content(prompt, retry=retry_strategy)
        return response.text.strip()
    except DeadlineExceeded as e:
        # Log the timeout error
        print(f"Error: Timeout occurred while generating response. {e}")
        return "Sorry, the request timed out. Please try again later."
    except Exception as e:
        # Log any other error
        print(f"Error: An unexpected error occurred. {e}")
        return "An error occurred. Please try again later."

