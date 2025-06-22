def get_writer_prompt(text, style_preferences=None):
    """Enhanced writer prompt with style guidelines"""
    prompt = f"""You are an expert content writer specializing in modernizing classic literature while preserving its essence.

TASK: Rewrite the following text in modern, engaging prose that appeals to contemporary readers.

GUIDELINES:
✅ Preserve the original meaning and narrative flow
✅ Update archaic language to modern equivalents
✅ Improve readability while maintaining literary quality
✅ Keep the original tone and style intent
✅ Ensure smooth transitions between paragraphs
✅ Use active voice where appropriate

STYLE REQUIREMENTS:
- Target audience: Modern adult readers
- Reading level: Accessible but sophisticated
- Tone: Engaging yet respectful to the original
- Length: Similar to original (±20%)

{f"ADDITIONAL STYLE PREFERENCES: {style_preferences}" if style_preferences else ""}

ORIGINAL TEXT:
{text}

REWRITTEN VERSION:"""

    return prompt

def get_reviewer_prompt(text, original_text=None):
    """Enhanced reviewer prompt with detailed criteria and direct instructions."""
    prompt = f"""You are a professional editor. Your task is to review and improve the provided text.

REVIEW CHECKLIST (internal monologue, do not include in output):
- Coherence: Does the text flow logically?
- Grammar: Are there any grammatical errors?
- Style: Is the style consistent and engaging?
- Accuracy: Does it preserve the original meaning?
- Readability: Is it easy for a modern reader to understand?

INSTRUCTIONS:
1. Read the text carefully.
2. Apply improvements based on the checklist above.
3. **Your final output must be ONLY the polished, improved version of the text.**
4. Do NOT include your review, comments, or any extra text.

TEXT TO REVIEW AND IMPROVE:
{text}

{f"ORIGINAL TEXT FOR CONTEXT: {original_text[:500]}..." if original_text else ""}

IMPROVED TEXT:"""

    return prompt

def get_editor_prompt(text, feedback=None):
    """Enhanced editor prompt with specific focus areas"""
    prompt = f"""You are a professional editor applying final polish to reviewed content.

EDITORIAL OBJECTIVES:
🎯 Apply final stylistic improvements
🎨 Ensure consistent tone and voice throughout
✨ Polish language for maximum impact and clarity
📚 Maintain professional publication standards
🔧 Fix any remaining issues

EDITING FOCUS AREAS:
- Sentence structure optimization
- Word choice refinement and precision
- Punctuation and formatting consistency
- Paragraph flow and transitions
- Overall narrative coherence
- Final proofreading

{f"SPECIFIC FEEDBACK TO ADDRESS: {feedback}" if feedback else ""}

QUALITY STANDARDS:
- Publication-ready quality
- Consistent voice and tone
- Optimal readability
- Professional presentation

TEXT TO EDIT:
{text}

FINAL POLISHED VERSION:"""

    return prompt

def get_regeneration_prompt(text, feedback):
    """Specialized prompt for feedback-based regeneration"""
    return f"""You are tasked with revising content based on specific human feedback.

HUMAN FEEDBACK TO ADDRESS:
"{feedback}"

REVISION INSTRUCTIONS:
🎯 Focus specifically on the areas mentioned in the feedback
✅ Address all points raised by the human reviewer
🔄 Maintain the overall structure and meaning
⚡ Make targeted improvements rather than wholesale changes
📝 Ensure the revision directly responds to the feedback

ORIGINAL TEXT:
{text}

REVISED VERSION ADDRESSING THE FEEDBACK:"""