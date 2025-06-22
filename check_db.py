#!/usr/bin/env python3
"""
Quick database checker script to see what content is stored in ChromaDB
"""

import sys
import os
from datetime import datetime

def check_database():
    """Check what's currently stored in the ChromaDB database"""

    try:
        # Import ChromaDB handler
        from storage.chromadb_handler import collection, get_statistics

        print("🔍 CHROMADB DATABASE STATUS")
        print("=" * 50)

        # Get basic stats
        try:
            doc_count = collection.count()
            print(f"📚 Total documents: {doc_count}")
        except Exception as e:
            print(f"❌ Error getting document count: {e}")
            return False

        if doc_count == 0:
            print("\n📭 DATABASE IS EMPTY")
            print("   No content has been processed yet.")
            print("\n💡 To add content:")
            print("   python main.py --mode process --url \"https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1\"")
            return True

        # Get all stored documents
        print(f"\n📄 STORED DOCUMENTS:")
        print("-" * 30)

        try:
            results = collection.get()

            if results and results.get('documents'):
                documents = results['documents']
                metadatas = results.get('metadatas', [{}] * len(documents))
                ids = results.get('ids', [f"doc_{i}" for i in range(len(documents))])

                for i, (doc_id, doc, metadata) in enumerate(zip(ids, documents, metadatas), 1):
                    print(f"\n{i}. ID: {doc_id}")

                    # Show metadata
                    if metadata:
                        url = metadata.get('url', 'Unknown')
                        timestamp = metadata.get('timestamp', 'Unknown')
                        char_count = metadata.get('char_count', len(doc))
                        word_count = metadata.get('word_count', len(doc.split()))

                        print(f"   🔗 URL: {url}")
                        print(f"   📅 Stored: {timestamp}")
                        print(f"   📊 Stats: {char_count} chars, {word_count} words")

                    # Show content preview
                    preview = doc[:200] if len(doc) > 200 else doc
                    print(f"   📝 Preview: {preview}...")

                    if i < len(documents):
                        print("-" * 30)

        except Exception as e:
            print(f"❌ Error getting documents: {e}")
            return False

        # Show statistics if available
        print(f"\n📊 DETAILED STATISTICS:")
        print("-" * 25)
        try:
            get_statistics()
        except Exception as e:
            print(f"⚠️ Could not get detailed statistics: {e}")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and dependencies are installed.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_search_functionality():
    """Test if search would work with current database"""

    try:
        from storage.chromadb_handler import retrieve_best_match

        print(f"\n🔍 TESTING SEARCH FUNCTIONALITY:")
        print("-" * 35)

        # Try a test search
        test_query = "test content"
        result = retrieve_best_match(test_query)

        if result == "No match found.":
            print("❌ Search returns: No match found")
            print("   This is expected if database is empty")
        else:
            print("✅ Search functionality working")
            print(f"   Test result preview: {result[:100]}...")

        return True

    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False

def suggest_next_steps():
    """Suggest what to do next based on database status"""

    print(f"\n💡 NEXT STEPS:")
    print("=" * 20)

    try:
        from storage.chromadb_handler import collection
        doc_count = collection.count()

        if doc_count == 0:
            print("1. Process some content first:")
            print("   python main.py --mode process --url \"https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1\"")
            print("\n2. Then try searching:")
            print("   python main.py --mode search --query \"your search term\"")

        else:
            print("1. Your database has content! Try searching:")
            print("   python main.py --mode search --query \"character analysis\"")
            print("   python main.py --mode search --query \"descriptive passages\"")
            print("   python main.py --mode search --query \"dialogue scenes\"")
            print("\n2. Process more content to improve search:")
            print("   python main.py --mode process --url \"https://another-url.com\"")
            print("\n3. Remember to rate search results to train the RL system!")

    except Exception as e:
        print(f"⚠️ Could not determine database status: {e}")
        print("1. Try running the test script: python test_system.py --quick")
        print("2. Check your setup and dependencies")

if __name__ == "__main__":
    print(f"🚀 ChromaDB Database Checker")
    print(f"Started at: {datetime.now()}")
    print("=" * 60)

    success = check_database()

    if success:
        test_search_functionality()
        suggest_next_steps()

    print("\n" + "=" * 60)
    print("✨ Database check completed!")