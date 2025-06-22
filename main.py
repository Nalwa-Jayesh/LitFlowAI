from scraper.fetcher import fetch_chapter_content
from ai_agents.writer import ai_writer
from ai_agents.reviewer import ai_reviewer
from ai_agents.editor import ai_editor
from interface.human_loop import human_review_loop
from storage.chromadb_handler import (
    save_version, retrieve_best_match, submit_feedback,
    list_versions_for_url, delete_version_by_id, set_active_version
)
import argparse
import logging
from datetime import datetime


def process_chapter(url, max_iterations=3):
    """Enhanced chapter processing with better error handling"""
    print(f"🚀 Starting chapter processing: {url}")

    try:
        # Step 1: Fetch content
        print("🔍 Fetching chapter content...")
        raw_html, plain_text = fetch_chapter_content(url)
        print(f"✅ Fetched {len(plain_text)} characters")

        # Step 2: AI Processing Pipeline
        print("\n🤖 AI Processing Pipeline:")

        print("   📝 AI Writer processing...")
        spun = ai_writer(plain_text)
        print(f"   ✅ Writer complete ({len(spun)} chars)")

        print("   🔍 AI Reviewer processing...")
        reviewed = ai_reviewer(spun)
        print(f"   ✅ Reviewer complete ({len(reviewed)} chars)")

        print("   ✨ AI Editor processing...")
        edited = ai_editor(reviewed)
        print(f"   ✅ Editor complete ({len(edited)} chars)")

        # Step 3: Enhanced Human Review
        print(f"\n👥 Starting Human Review Process (max {max_iterations} iterations)...")
        final = human_review_loop(plain_text, spun, reviewed, edited, max_iterations)

        # Step 4: Save final version
        print("\n💾 Saving final version...")
        save_version(url, final)
        print("✅ Version saved successfully")

        return final

    except Exception as e:
        logging.error(f"Error processing chapter: {e}")
        print(f"❌ Error: {e}")
        return None


def search_content(query):
    """Enhanced search with better feedback collection"""
    print(f"🔍 Searching for: '{query}'")

    try:
        best_match = retrieve_best_match(query)

        if best_match == "No match found.":
            print("❌ No matching content found.")
            return

        print(f"\n{'='*60}")
        print("📄 BEST MATCHED CONTENT")
        print(f"{'='*60}")
        print(best_match[:1000])  # Show more content
        if len(best_match) > 1000:
            print("\n[Content truncated for display...]")
        print(f"{'='*60}")

        # Enhanced feedback collection
        print("\n💭 Please rate this result:")
        print("1 = Very Poor | 2 = Poor | 3 = Average | 4 = Good | 5 = Excellent")

        while True:
            try:
                rating = input("Rating (1-5): ").strip()
                rating_num = int(rating)
                if 1 <= rating_num <= 5:
                    # Convert to reward scale (-1 to 1)
                    reward = (rating_num - 3) / 2  # Maps 1->-1, 3->0, 5->1
                    submit_feedback(query, best_match, reward)
                    print(f"✅ Thank you! Rating: {rating_num}/5 (reward: {reward})")
                    break
                else:
                    print("Please enter a number between 1 and 5")
            except ValueError:
                print("Please enter a valid number")

    except Exception as e:
        logging.error(f"Error during search: {e}")
        print(f"❌ Search error: {e}")


def manage_versions(args):
    """Handle version management tasks."""
    print(f"🛠️ Version Management Mode (Action: {args.action})")

    if args.action == 'list':
        if not args.url:
            print("❌ Please provide --url for list action")
            return
        
        versions = list_versions_for_url(args.url)
        if versions:
            print(f"\nFound {len(versions['ids'])} version(s):")
            for i, doc_id in enumerate(versions['ids']):
                meta = versions['metadatas'][i]
                doc = versions['documents'][i]
                status = "✅ ACTIVE" if meta.get('is_active') else " archived"
                print(f"\n[{i+1}] ID: {doc_id} ({status})")
                print(f"    - Timestamp: {meta.get('timestamp')}")
                print(f"    - Preview: {doc[:100].strip()}...")

    elif args.action == 'delete':
        if not args.id:
            print("❌ Please provide --id for delete action")
            return
        delete_version_by_id(args.id)

    elif args.action == 'activate':
        if not args.id:
            print("❌ Please provide --id for activate action")
            return
        set_active_version(args.id)

    else:
        print(f"❌ Invalid action '{args.action}'. Choose from: list, delete, activate")


if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description="Enhanced AI Publishing System")
    parser.add_argument('--mode', type=str, choices=['process', 'search', 'manage'], required=True,
                      help='Choose mode: process, search, or manage versions')
    parser.add_argument('--url', type=str, help='Chapter URL for processing or listing versions')
    parser.add_argument('--query', type=str, help='Query to search in stored content')
    parser.add_argument('--iterations', type=int, default=3,
                      help='Maximum human review iterations (default: 3)')
    parser.add_argument('--action', type=str, choices=['list', 'delete', 'activate'],
                      help='Management action to perform (for --mode manage)')
    parser.add_argument('--id', type=str,
                      help='Document ID for delete/activate actions')

    args = parser.parse_args()

    if args.mode == 'process':
        if not args.url:
            print("❌ Please provide --url for processing mode")
            exit(1)

        print(f"🎯 Processing Mode: {args.url}")
        final_output = process_chapter(args.url, args.iterations)

        if final_output:
            print(f"\n{'='*60}")
            print("🎉 FINAL CHAPTER OUTPUT")
            print(f"{'='*60}")
            print(final_output)
            print(f"\n📊 Final length: {len(final_output)} characters")

    elif args.mode == 'search':
        if not args.query:
            print("❌ Please provide --query for search mode")
            exit(1)

        print(f"🔍 Search Mode: '{args.query}'")
        search_content(args.query)

    elif args.mode == 'manage':
        manage_versions(args)

    print("\n✨ Operation completed!")