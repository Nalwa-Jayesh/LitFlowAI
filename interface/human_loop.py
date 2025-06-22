import json
from datetime import datetime

def human_review_loop(original, spun, reviewed, edited, max_iterations=3):
    """Enhanced human-in-the-loop with multiple iterations"""

    versions = {
        "original": original,
        "ai_spun": spun,
        "ai_reviewed": reviewed,
        "ai_edited": edited
    }

    current_version = edited  # Start with AI's best effort
    iteration = 1

    while iteration <= max_iterations:
        print(f"\n{'='*60}")
        print(f"🔄 HUMAN REVIEW - ITERATION {iteration}/{max_iterations}")
        print(f"{'='*60}")

        # Display versions for comparison
        display_versions(versions, current_version, iteration)

        # Get human decision
        decision = get_human_decision()

        if decision == "accept":
            print("✅ Version accepted!")
            log_decision(iteration, decision, current_version)
            return current_version

        elif decision == "edit":
            print("\n✏️ MANUAL EDIT MODE")
            current_version = get_manual_edit(current_version)
            versions[f"human_edit_v{iteration}"] = current_version
            log_decision(iteration, decision, current_version)

        elif decision == "regenerate":
            print("\n🔄 AI REGENERATION WITH FEEDBACK")
            current_version = regenerate_with_feedback(current_version)
            versions[f"ai_regen_v{iteration}"] = current_version
            log_decision(iteration, decision, current_version)

        elif decision == "revert":
            current_version = select_previous_version(versions)
            log_decision(iteration, decision, current_version)

        elif decision == "compare":
            compare_versions(versions)
            continue  # Don't increment iteration for comparison

        iteration += 1

    print(f"⚠️ Max iterations ({max_iterations}) reached. Using current version.")
    return current_version

def display_versions(versions, current, iteration):
    """Display version previews with better formatting"""
    print(f"\n📚 VERSION COMPARISON (Iteration {iteration}):")
    print("-" * 60)

    for name, text in versions.items():
        status = "🔄 CURRENT" if text == current else "📄"
        print(f"\n{status} {name.upper().replace('_', ' ')}:")
        print(f"   Length: {len(text)} chars | Words: {len(text.split())}")
        print(f"   Preview: {text[:150]}...")
        if len(text) > 150:
            print("   [...]")

    print(f"\n🎯 CURRENT WORKING VERSION:")
    print(f"   {current[:200]}...")
    print("-" * 60)

def get_human_decision():
    """Get human decision with better UX"""
    print("\n🤔 What would you like to do?")
    print("   1. 'accept'     - ✅ Accept current version")
    print("   2. 'edit'       - ✏️ Manually edit current version")
    print("   3. 'regenerate' - 🔄 Ask AI to regenerate with feedback")
    print("   4. 'revert'     - ⏪ Go back to a previous version")
    print("   5. 'compare'    - 🔍 Compare all versions side-by-side")

    while True:
        choice = input("\n👉 Enter your choice: ").strip().lower()
        if choice in ["accept", "edit", "regenerate", "revert", "compare"]:
            return choice
        print("❌ Invalid choice. Please use: accept, edit, regenerate, revert, or compare")

def get_manual_edit(current_version):
    """Enhanced manual editing with options"""
    print(f"\n📝 CURRENT VERSION ({len(current_version)} chars):")
    print("-" * 40)
    print(current_version)
    print("-" * 40)

    print("\nEDITING OPTIONS:")
    print("1. Type 'replace' to replace entire text")
    print("2. Type 'keep' to keep current version")
    print("3. Or paste your edited version below:")

    user_input = input("\n✏️ Your input: ").strip()

    if user_input.lower() == 'keep':
        return current_version
    elif user_input.lower() == 'replace':
        print("\n📝 Enter your complete replacement text:")
        return input().strip()
    elif user_input:
        return user_input
    else:
        print("No changes made. Keeping current version.")
        return current_version

def regenerate_with_feedback(current_version):
    """Regenerate with AI based on human feedback"""
    print("🔄 What specific improvements would you like?")
    print("Examples: 'make it more formal', 'simplify the language', 'add more detail'")

    feedback = input("\n💬 Your feedback: ").strip()

    if not feedback:
        print("No feedback provided. Keeping current version.")
        return current_version

    enhanced_prompt = f"""Please revise this text based on the following specific feedback: {feedback}

ORIGINAL TEXT:
{current_version}

REVISED VERSION ADDRESSING THE FEEDBACK:"""

    print("🤖 AI is processing your feedback...")
    try:
        from utils.gemini_api import call_gemini
        improved_version = call_gemini(enhanced_prompt)
        print("✅ AI regeneration complete!")
        return improved_version
    except Exception as e:
        print(f"❌ AI regeneration failed: {e}")
        return current_version

def select_previous_version(versions):
    """Enhanced version selection"""
    print("\n⏪ SELECT PREVIOUS VERSION:")
    version_list = list(versions.items())

    for i, (name, text) in enumerate(version_list, 1):
        word_count = len(text.split())
        print(f"   {i}. {name.replace('_', ' ').title()} ({word_count} words)")
        print(f"      Preview: {text[:100]}...")

    while True:
        try:
            choice = input(f"\n👉 Select version (1-{len(version_list)}): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(version_list):
                selected_name, selected_text = version_list[choice_num-1]
                print(f"✅ Reverted to: {selected_name.replace('_', ' ').title()}")
                return selected_text
        except ValueError:
            pass
        print(f"❌ Please enter a number between 1 and {len(version_list)}")

def compare_versions(versions):
    """Side-by-side version comparison"""
    print(f"\n🔍 DETAILED VERSION COMPARISON:")
    print("=" * 80)

    version_items = list(versions.items())

    for i, (name, text) in enumerate(version_items):
        print(f"\n📄 {i+1}. {name.upper().replace('_', ' ')}")
        print(f"   📊 Stats: {len(text)} chars, {len(text.split())} words")
        print(f"   📝 Text: {text[:300]}...")
        if i < len(version_items) - 1:
            print("-" * 60)

    input("\n⏎ Press Enter to continue...")

def log_decision(iteration, decision, version):
    """Log human decisions for analysis"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "iteration": iteration,
        "decision": decision,
        "version_length": len(version),
        "version_preview": version[:100]
    }

    # In a real system, you'd save this to a database
    print(f"📝 Logged: Iteration {iteration} - {decision}")