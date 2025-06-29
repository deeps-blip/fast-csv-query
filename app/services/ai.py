import google.generativeai as genai
from app.core.config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_question(question: str, context: str) -> str:
    try:
        prompt = f"Based on the following data:\n{context}\nAnswer the question: {question}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
