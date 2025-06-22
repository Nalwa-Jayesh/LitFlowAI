from utils.prompts import get_writer_prompt
from utils.gemini_api import call_gemini


def ai_writer(text, style_preferences=None):
    """Enhanced AI writer with style preferences and error handling"""
    try:
        print("📝 AI Writer: Processing text...")
        prompt = get_writer_prompt(text, style_preferences)
        result = call_gemini(prompt)
        print("✅ AI Writer: Complete")
        return result
    except Exception as e:
        print(f"❌ AI Writer Error: {e}")
        return f"AI Writer Error: Could not process the text. Original text preserved:\n\n{text}"