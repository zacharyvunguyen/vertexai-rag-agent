#!/usr/bin/env python3
"""
Script to test queries against the Student Report Card RAG corpus.
Useful for validating corpus content and testing query performance.
"""

import os
import argparse
from dotenv import load_dotenv
from vertexai import rag
import vertexai

# Load environment variables
load_dotenv()

# Initialize Vertex AI
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION")
RAG_CORPUS_NAME = os.environ.get("RAG_CORPUS_NAME")

print(f"Initializing Vertex AI with project={PROJECT_ID}, location={LOCATION}")
vertexai.init(project=PROJECT_ID, location=LOCATION)

def get_corpus_resource_name():
    """Get the full resource name of the corpus."""
    try:
        corpora = rag.list_corpora()
        for corpus in corpora:
            if corpus.display_name == RAG_CORPUS_NAME:
                return corpus.name
        return None
    except Exception as e:
        print(f"   ❌ Error finding corpus: {str(e)}")
        return None

def query_corpus(query_text, top_k=5, distance_threshold=0.5):
    """Query the RAG corpus and return results."""
    try:
        # Get corpus resource name
        corpus_resource_name = get_corpus_resource_name()
        if not corpus_resource_name:
            print(f"   ❌ Corpus '{RAG_CORPUS_NAME}' not found.")
            return None
        
        print(f"\n🔍 Querying corpus: {RAG_CORPUS_NAME}")
        print(f"   Query: '{query_text}'")
        print(f"   Top K: {top_k}")
        print(f"   Distance threshold: {distance_threshold}")
        
        # Configure retrieval parameters
        rag_retrieval_config = rag.RagRetrievalConfig(
            top_k=top_k,
            filter=rag.Filter(vector_distance_threshold=distance_threshold),
        )
        
        # Perform the query
        response = rag.retrieval_query(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=corpus_resource_name,
                )
            ],
            text=query_text,
            rag_retrieval_config=rag_retrieval_config,
        )
        
        # Process results
        results = []
        if hasattr(response, "contexts") and response.contexts:
            for i, ctx_group in enumerate(response.contexts.contexts):
                result = {
                    "rank": i + 1,
                    "source_uri": getattr(ctx_group, "source_uri", ""),
                    "source_name": getattr(ctx_group, "source_display_name", ""),
                    "text": getattr(ctx_group, "text", ""),
                    "score": getattr(ctx_group, "score", 0.0),
                }
                results.append(result)
        
        return results
        
    except Exception as e:
        print(f"   ❌ Error querying corpus: {str(e)}")
        return None

def display_results(results):
    """Display query results in a formatted way."""
    if not results:
        print("\n   ⚠️  No results found for this query.")
        print("   Try:")
        print("     - Different keywords")
        print("     - Lower distance threshold")
        print("     - Adding more documents to corpus")
        return
    
    print(f"\n📋 Found {len(results)} results:")
    print("=" * 80)
    
    for result in results:
        print(f"\n🔹 Result #{result['rank']} (Score: {result['score']:.3f})")
        
        if result['source_name']:
            print(f"   📄 Source: {result['source_name']}")
        if result['source_uri']:
            print(f"   🔗 URI: {result['source_uri']}")
        
        # Display text content with truncation
        text = result['text'].strip()
        if len(text) > 300:
            text = text[:300] + "..."
        
        print(f"   📝 Content:")
        print(f"      {text}")
        print("-" * 80)

def interactive_mode():
    """Run in interactive mode for multiple queries."""
    print("\n🔄 Interactive Query Mode")
    print("   Type 'quit' to exit")
    print("   Type 'help' for sample queries")
    print("-" * 60)
    
    sample_queries = [
        "What does 'approaching standard' mean in math?",
        "How can parents help with reading comprehension?",
        "Explain the grading scale used in elementary school",
        "What are the benchmarks for first grade students?",
        "How is social studies performance measured?",
    ]
    
    while True:
        try:
            query = input("\n💬 Enter your query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("   👋 Goodbye!")
                break
            elif query.lower() == 'help':
                print("\n📝 Sample queries to try:")
                for i, sample in enumerate(sample_queries, 1):
                    print(f"   {i}. {sample}")
                continue
            elif not query:
                continue
            
            # Perform query
            results = query_corpus(query)
            display_results(results)
            
        except KeyboardInterrupt:
            print("\n   👋 Goodbye!")
            break
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description="Test queries against the Student Report Card RAG corpus"
    )
    parser.add_argument(
        "--query",
        help="Single query to test"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of top results to return (default: 5)"
    )
    parser.add_argument(
        "--distance-threshold",
        type=float,
        default=0.5,
        help="Vector distance threshold (default: 0.5)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("🔍 Student Report Card RAG - Query Testing")
    print("="*60)
    
    # Check if corpus exists
    corpus_resource_name = get_corpus_resource_name()
    if not corpus_resource_name:
        print(f"\n❌ Corpus '{RAG_CORPUS_NAME}' not found!")
        print("   Please create the corpus first with:")
        print("   python check_corpus.py")
        return 1
    
    if args.query:
        # Single query mode
        results = query_corpus(
            args.query, 
            top_k=args.top_k, 
            distance_threshold=args.distance_threshold
        )
        display_results(results)
        
    elif args.interactive:
        # Interactive mode
        interactive_mode()
        
    else:
        # Default: show sample queries and enter interactive mode
        print("\n📝 Sample queries for testing:")
        sample_queries = [
            "What does 'approaching standard' mean in math?",
            "How can parents help with reading comprehension?",
            "Explain the grading scale used in elementary school",
            "What are the benchmarks for first grade students?",
        ]
        
        for i, sample in enumerate(sample_queries, 1):
            print(f"   {i}. {sample}")
        
        print(f"\n🎯 Testing with sample query...")
        results = query_corpus(sample_queries[0])
        display_results(results)
        
        # Ask if user wants interactive mode
        try:
            response = input("\n❓ Enter interactive mode? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                interactive_mode()
        except KeyboardInterrupt:
            print("\n   👋 Goodbye!")
    
    print("\n" + "="*60)
    print("📋 Query testing completed!")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    exit(main()) 