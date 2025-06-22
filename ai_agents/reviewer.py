from utils.prompts import get_reviewer_prompt
from utils.gemini_api import call_gemini


def ai_reviewer(text, original_text=None):
    """Enhanced AI reviewer with original text reference and error handling"""
    try:
        print("🔍 AI Reviewer: Analyzing text...")
        prompt = get_reviewer_prompt(text, original_text)
        result = call_gemini(prompt)
        print("✅ AI Reviewer: Complete")
        return result
    except Exception as e:
        print(f"❌ AI Reviewer Error: {e}")
        return f"AI Reviewer Error: Could not review the text. Original text preserved:\n\n{text}"