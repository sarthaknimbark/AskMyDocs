import google.generativeai as genai

def get_gemini_response(context, question):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    prompt = f"""Use the following context to answer the question below.

Context:
{context}

Question: {question}
Answer:"""
    response = model.generate_content(prompt)
    return response.text.strip()
