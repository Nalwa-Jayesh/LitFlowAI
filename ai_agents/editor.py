from utils.prompts import get_editor_prompt
from utils.gemini_api import call_gemini


def ai_editor(text, feedback=None):
    """Enhanced AI editor with feedback support and error handling"""
    try:
        print("✨ AI Editor: Polishing text...")
        prompt = get_editor_prompt(text, feedback)
        result = call_gemini(prompt)
        print("✅ AI Editor: Complete")
        return result
    except Exception as e:
        print(f"❌ AI Editor Error: {e}")
        return f"AI Editor Error: Could not edit the text. Original text preserved:\n\n{text}"