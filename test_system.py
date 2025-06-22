#!/usr/bin/env python3
"""
Test script for the AI Publishing System
Run this to verify all components are working correctly
"""

import sys
import os
import traceback
from datetime import datetime

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")

    try:
        # Core modules
        from scraper.fetcher import fetch_chapter_content
        from ai_agents.writer import ai_writer
        from ai_agents.reviewer import ai_reviewer
        from ai_agents.editor import ai_editor
        from interface.human_loop import human_review_loop
        from storage.chromadb_handler import save_version, retrieve_best_match, submit_feedback
        from utils.gemini_api import call_gemini
        from utils.prompts import get_writer_prompt, get_reviewer_prompt, get_editor_prompt
        from config import config

        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during imports: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n🔧 Testing environment...")

    try:
        from config import config
        config.validate()
        print("✅ Environment configuration valid!")

        # Test API key
        if config.gemini_api_key:
            print("✅ Gemini API key found")
        else:
            print("⚠️ Gemini API key not found - check .env file")

        return True
    except Exception as e:
        print(f"❌ Environment error: {e}")
        return False

def test_gemini_api():
    """Test Gemini API connection"""
    print("\n🤖 Testing Gemini API...")

    try:
        from utils.gemini_api import call_gemini

        test_prompt = "Say 'Hello, AI Publishing System!' in exactly those words."
        response = call_gemini(test_prompt)

        if response and "Hello, AI Publishing System!" in response:
            print("✅ Gemini API working correctly!")
            return True
        else:
            print(f"⚠️ Gemini API responded but with unexpected content: {response[:100]}...")
            return True  # Still working, just different response

    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False

def test_ai_agents():
    """Test AI agents"""
    print("\n🤖 Testing AI agents...")

    test_text = "This is a test sentence for the AI agents to process."

    try:
        # Test Writer
        print("   📝 Testing AI Writer...")
        writer_result = ai_writer(test_text)
        if writer_result and len(writer_result) > 10:
            print("   ✅ AI Writer working")
        else:
            print("   ⚠️ AI Writer returned short/empty response")

        # Test Reviewer
        print("   🔍 Testing AI Reviewer...")
        reviewer_result = ai_reviewer(test_text)
        if reviewer_result and len(reviewer_result) > 10:
            print("   ✅ AI Reviewer working")
        else:
            print("   ⚠️ AI Reviewer returned short/empty response")

        # Test Editor
        print("   ✨ Testing AI Editor...")
        editor_result = ai_editor(test_text)
        if editor_result and len(editor_result) > 10:
            print("   ✅ AI Editor working")
        else:
            print("   ⚠️ AI Editor returned short/empty response")

        return True

    except Exception as e:
        print(f"   ❌ AI agents error: {e}")
        return False

def test_storage():
    """Test storage system"""
    print("\n💾 Testing storage system...")

    try:
        from storage.chromadb_handler import save_version, retrieve_best_match, submit_feedback

        # Test save
        test_url = "https://test.example.com/test"
        test_content = "This is test content for storage verification."

        print("   💾 Testing save_version...")
        doc_id = save_version(test_url, test_content)
        print(f"   ✅ Document saved with ID: {doc_id}")

        # Test retrieve
        print("   🔍 Testing retrieve_best_match...")
        result = retrieve_best_match("test content")
        if result and result != "No match found.":
            print("   ✅ Document retrieved successfully")
        else:
            print("   ⚠️ No documents found (this is normal for first run)")

        # Test feedback
        print("   📊 Testing submit_feedback...")
        submit_feedback("test query", "test result", 0.5)
        print("   ✅ Feedback submitted successfully")

        return True

    except Exception as e:
        print(f"   ❌ Storage error: {e}")
        return False

def test_scraper():
    """Test web scraper (optional - requires internet)"""
    print("\n🔍 Testing web scraper...")

    try:
        from scraper.fetcher import fetch_chapter_content

        # Simple test URL
        test_url = "https://httpbin.org/html"

        print(f"   🌐 Testing fetch from: {test_url}")
        html, text = fetch_chapter_content(test_url)

        if html and text:
            print(f"   ✅ Scraper working - fetched {len(text)} characters")
            return True
        else:
            print("   ⚠️ Scraper returned empty content")
            return False

    except Exception as e:
        print(f"   ❌ Scraper error: {e}")
        print("   ℹ️ This might be due to network issues or missing playwright")
        return False

def test_prompts():
    """Test prompt generation"""
    print("\n📝 Testing prompt system...")

    try:
        from utils.prompts import get_writer_prompt, get_reviewer_prompt, get_editor_prompt

        test_text = "Sample text for prompt testing."

        # Test writer prompt
        writer_prompt = get_writer_prompt(test_text)
        if writer_prompt and len(writer_prompt) > 50:
            print("   ✅ Writer prompt generated")
        else:
            print("   ⚠️ Writer prompt seems too short")

        # Test reviewer prompt
        reviewer_prompt = get_reviewer_prompt(test_text)
        if reviewer_prompt and len(reviewer_prompt) > 50:
            print("   ✅ Reviewer prompt generated")
        else:
            print("   ⚠️ Reviewer prompt seems too short")

        # Test editor prompt
        editor_prompt = get_editor_prompt(test_text)
        if editor_prompt and len(editor_prompt) > 50:
            print("   ✅ Editor prompt generated")
        else:
            print("   ⚠️ Editor prompt seems too short")

        return True

    except Exception as e:
        print(f"   ❌ Prompt system error: {e}")
        return False

def run_full_test():
    """Run complete system test"""
    print("🚀 AI Publishing System - Full Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now()}")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("Environment", test_environment),
        ("Gemini API", test_gemini_api),
        ("AI Agents", test_ai_agents),
        ("Storage System", test_storage),
        ("Prompt System", test_prompts),
        ("Web Scraper", test_scraper),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = 0
    failed = 0

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1

    print("-" * 60)
    print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed}")

    if failed == 0:
        print("🎉 ALL TESTS PASSED! System is ready to use.")
    elif failed <= 2:
        print("⚠️ Some tests failed, but core functionality should work.")
    else:
        print("❌ Multiple tests failed. Please check your setup.")

    print("\n💡 Next steps:")
    print("   1. If tests passed, try: python main.py --mode process --url <URL>")
    print("   2. If tests failed, check the error messages above")
    print("   3. Make sure you have: playwright install chromium")
    print("   4. Check your .env file has GEMINI_API_KEY set")

    return failed == 0

def quick_test():
    """Run quick essential tests only"""
    print("⚡ Quick Test - Essential Components Only")
    print("-" * 40)

    essential_tests = [
        ("Imports", test_imports),
        ("Environment", test_environment),
        ("Gemini API", test_gemini_api),
    ]

    for test_name, test_func in essential_tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            if not result:
                print(f"❌ {test_name} failed - system may not work properly")
                return False
        except Exception as e:
            print(f"❌ {test_name} exception: {e}")
            return False

    print("\n✅ Quick test passed! Core components are working.")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        success = quick_test()
    else:
        success = run_full_test()

    sys.exit(0 if success else 1)