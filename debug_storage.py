#!/usr/bin/env python3
"""
Debug storage script to diagnose ChromaDB and search issues
"""

import sys
import os
import traceback
from datetime import datetime

def debug_chromadb():
    """Debug ChromaDB connection and data"""
    print("🔍 DEBUGGING CHROMADB")
    print("=" * 40)

    try:
        import chromadb
        print("✅ ChromaDB import successful")

        # Test client connection
        client = chromadb.Client()
        print("✅ ChromaDB client created")

        # Check collections
        collections = client.list_collections()
        print(f"📚 Collections found: {len(collections)}")

        for collection in collections:
            print(f"   - {collection.name}")

        # Get our specific collection
        collection = client.get_or_create_collection(name="chapters")
        print(f"✅ 'chapters' collection accessed")

        # Check document count
        doc_count = collection.count()
        print(f"📄 Documents in collection: {doc_count}")

        if doc_count > 0:
            # Get all documents
            results = collection.get()
            print(f"📋 Retrieved {len(results.get('documents', []))} documents")

            for i, doc in enumerate(results.get('documents', [])[:3]):  # Show first 3
                print(f"\n📄 Document {i+1}:")
                print(f"   Length: {len(doc)} chars")
                print(f"   Preview: {doc[:100]}...")

                # Check metadata
                metadata = results.get('metadatas', [{}])[i] if i < len(results.get('metadatas', [])) else {}
                if metadata:
                    print(f"   URL: {metadata.get('url', 'None')}")
                    print(f"   Timestamp: {metadata.get('timestamp', 'None')}")

        return True

    except Exception as e:
        print(f"❌ ChromaDB error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def debug_embeddings():
    """Debug embedding model"""
    print("\n🧠 DEBUGGING EMBEDDINGS")
    print("=" * 40)

    try:
        from sentence_transformers import SentenceTransformer
        print("✅ SentenceTransformers import successful")

        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded")

        # Test embedding
        test_text = "This is a test sentence"
        embedding = model.encode(test_text)
        print(f"✅ Test embedding created: shape {embedding.shape}")

        return True

    except Exception as e:
        print(f"❌ Embedding error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def debug_storage_functions():
    """Debug storage handler functions"""
    print("\n💾 DEBUGGING STORAGE FUNCTIONS")
    print("=" * 40)

    try:
        from storage.chromadb_handler import save_version, retrieve_best_match, submit_feedback
        print("✅ Storage functions imported")

        # Test save function
        print("🔄 Testing save_version...")
        test_url = "https://debug.test.com"
        test_content = "This is debug test content for troubleshooting the storage system."

        doc_id = save_version(test_url, test_content)
        print(f"✅ Test document saved: {doc_id}")

        # Test retrieve function
        print("🔄 Testing retrieve_best_match...")
        result = retrieve_best_match("debug test content")

        if result == "No match found.":
            print("❌ retrieve_best_match returned: No match found")
            return False
        else:
            print(f"✅ Retrieved content: {result[:100]}...")

        # Test feedback
        print("🔄 Testing submit_feedback...")
        submit_feedback("debug query", result, 0.5)
        print("✅ Feedback submitted")

        return True

    except Exception as e:
        print(f"❌ Storage functions error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def debug_main_workflow():
    """Debug main workflow integration"""
    print("\n🚀 DEBUGGING MAIN WORKFLOW")
    print("=" * 40)

    try:
        from main import process_chapter
        print("✅ Main workflow imported")

        # Check if process_chapter function exists and is callable
        if callable(process_chapter):
            print("✅ process_chapter function is callable")
        else:
            print("❌ process_chapter is not callable")
            return False

        return True

    except Exception as e:
        print(f"❌ Main workflow error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def debug_file_system():
    """Debug file system and paths"""
    print("\n📁 DEBUGGING FILE SYSTEM")
    print("=" * 40)

    # Check current directory
    current_dir = os.getcwd()
    print(f"📂 Current directory: {current_dir}")

    # Check for ChromaDB data files
    possible_db_paths = [
        "chromadb_data",
        "chroma.db",
        "chroma.sqlite3",
        ".chromadb"
    ]

    print("🔍 Looking for ChromaDB files:")
    for path in possible_db_paths:
        if os.path.exists(path):
            print(f"   ✅ Found: {path}")
            if os.path.isdir(path):
                files = os.listdir(path)
                print(f"      Contents: {files}")
        else:
            print(f"   ❌ Not found: {path}")

    # Check for model files
    model_files = ["rl_scoring_model.pkl", "*.model", "*.joblib"]
    print("\n🧠 Looking for ML model files:")
    for pattern in model_files:
        if "*" in pattern:
            import glob
            files = glob.glob(pattern)
            if files:
                print(f"   ✅ Found: {files}")
            else:
                print(f"   ❌ Not found: {pattern}")
        else:
            if os.path.exists(pattern):
                print(f"   ✅ Found: {pattern}")
            else:
                print(f"   ❌ Not found: {pattern}")

def debug_environment():
    """Debug environment variables and config"""
    print("\n🔧 DEBUGGING ENVIRONMENT")
    print("=" * 40)

    # Check Python version
    print(f"🐍 Python version: {sys.version}")

    # Check environment variables
    env_vars = ["GEMINI_API_KEY"]
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: Set (length: {len(value)})")
        else:
            print(f"❌ {var}: Not set")

    # Check config
    try:
        from config import config
        print("✅ Config imported")
        print(f"   Max iterations: {config.max_human_iterations}")
        print(f"   RL ranking enabled: {config.enable_rl_ranking}")
        print(f"   Gemini model: {config.gemini_model}")
    except Exception as e:
        print(f"❌ Config error: {e}")

def run_comprehensive_debug():
    """Run all debug tests"""
    print("🚀 COMPREHENSIVE STORAGE DEBUG")
    print("Started at:", datetime.now())
    print("=" * 60)

    tests = [
        ("Environment", debug_environment),
        ("File System", debug_file_system),
        ("ChromaDB", debug_chromadb),
        ("Embeddings", debug_embeddings),
        ("Storage Functions", debug_storage_functions),
        ("Main Workflow", debug_main_workflow),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            print(f"\n{'='*60}")
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))

    # Summary
    print(f"\n{'='*60}")
    print("📊 DEBUG SUMMARY")
    print("=" * 60)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    failed_tests = [name for name, result in results if not result]

    if not failed_tests:
        print("\n🎉 All debug tests passed!")
        print("💡 The issue might be in the workflow logic.")
        print("Try processing content again and check the output carefully.")
    else:
        print(f"\n❌ Failed tests: {', '.join(failed_tests)}")
        print("\n🔧 TROUBLESHOOTING STEPS:")

        if "ChromaDB" in failed_tests:
            print("   1. Reinstall ChromaDB: pip install --upgrade chromadb")
            print("   2. Delete any existing DB files and try again")

        if "Embeddings" in failed_tests:
            print("   1. Install sentence-transformers: pip install sentence-transformers")
            print("   2. Check internet connection for model download")

        if "Storage Functions" in failed_tests:
            print("   1. Check storage/chromadb_handler.py for syntax errors")
            print("   2. Verify all imports are working")

if __name__ == "__main__":
    run_comprehensive_debug()