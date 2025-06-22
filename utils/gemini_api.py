from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set! Please check your .env file.")
client = genai.Client(api_key=GEMINI_API_KEY)

def call_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # or "gemini-2.5-pro" if you have access
        contents=prompt
    )
    return response.text 