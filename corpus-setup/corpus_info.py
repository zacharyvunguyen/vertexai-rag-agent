#!/usr/bin/env python3
"""
Script to display detailed information about the Student Report Card RAG corpus.
Shows corpus statistics, document listings, and configuration details.
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

def list_all_corpora():
    """List all available corpora in the project."""
    try:
        print("\n🔍 Listing all available corpora...")
        corpora = rag.list_corpora()
        
        if not corpora:
            print("   No corpora found in this project.")
            return []
        
        corpus_list = list(corpora)
        print(f"   Found {len(corpus_list)} corpora:")
        corpus_info = []
        for corpus in corpus_list:
            print(f"\n   📚 {corpus.display_name}")
            print(f"      Resource: {corpus.name}")
            
            corpus_info.append({
                'display_name': corpus.display_name,
                'name': corpus.name,
                'corpus': corpus
            })
        
        return corpus_info
        
    except Exception as e:
        print(f"   ❌ Error listing corpora: {str(e)}")
        return []

def get_corpus_files(corpus_resource_name):
    """Get list of files in the corpus."""
    try:
        print(f"\n📁 Retrieving files from corpus...")
        
        # List files in the corpus
        files = rag.list_files(corpus_name=corpus_resource_name)
        
        file_details = []
        files_list = list(files)
        if files_list:
            print(f"   Found {len(files_list)} files:")
            for file in files_list:
                file_info = {
                    'name': getattr(file, 'name', 'Unknown'),
                    'display_name': getattr(file, 'display_name', 'Unknown'),
                    'size_bytes': getattr(file, 'size_bytes', 0),
                    'create_time': getattr(file, 'create_time', None),
                    'update_time': getattr(file, 'update_time', None),
                }
                file_details.append(file_info)
                
                print(f"\n   📄 {file_info['display_name']}")
                print(f"      Resource: {file_info['name']}")
                if file_info['size_bytes'] > 0:
                    size_mb = file_info['size_bytes'] / (1024 * 1024)
                    print(f"      Size: {size_mb:.2f} MB")
                if file_info['create_time']:
                    print(f"      Created: {file_info['create_time']}")
        else:
            print("   No files found in corpus.")
        
        return file_details
        
    except Exception as e:
        print(f"   ❌ Error listing files: {str(e)}")
        return []

def display_corpus_stats(corpus_info, file_details):
    """Display corpus statistics."""
    print("\n📊 Corpus Statistics")
    print("=" * 50)
    
    # Basic info
    print(f"Display Name: {corpus_info['display_name']}")
    print(f"Resource Name: {corpus_info['name']}")
    print(f"Project: {PROJECT_ID}")
    print(f"Location: {LOCATION}")
    
    # File statistics
    print(f"\nDocument Count: {len(file_details)}")
    
    if file_details:
        total_size = sum(file['size_bytes'] for file in file_details)
        total_size_mb = total_size / (1024 * 1024)
        print(f"Total Size: {total_size_mb:.2f} MB")
        
        avg_size_mb = total_size_mb / len(file_details) if file_details else 0
        print(f"Average File Size: {avg_size_mb:.2f} MB")
        
        # File types
        extensions = {}
        for file in file_details:
            name = file['display_name'].lower()
            if '.' in name:
                ext = '.' + name.split('.')[-1]
                extensions[ext] = extensions.get(ext, 0) + 1
        
        if extensions:
            print(f"\nFile Types:")
            for ext, count in sorted(extensions.items()):
                print(f"  {ext}: {count} files")
    
    # Configuration info
    print(f"\nConfiguration:")
    print(f"  Embedding Model: text-embedding-005")
    print(f"  Chunk Size: 512 tokens")
    print(f"  Chunk Overlap: 100 tokens")
    print(f"  Vector Database: Vertex AI RAG")

def display_detailed_files(file_details):
    """Display detailed file information."""
    if not file_details:
        print("\n   No files to display.")
        return
    
    print(f"\n📋 Detailed File Information")
    print("=" * 80)
    
    for i, file in enumerate(file_details, 1):
        print(f"\n📄 File #{i}: {file['display_name']}")
        print(f"   Resource ID: {file['name']}")
        
        if file['size_bytes'] > 0:
            size_mb = file['size_bytes'] / (1024 * 1024)
            print(f"   Size: {file['size_bytes']:,} bytes ({size_mb:.2f} MB)")
        
        if file['create_time']:
            print(f"   Created: {file['create_time']}")
        if file['update_time']:
            print(f"   Updated: {file['update_time']}")
        
        print("-" * 80)

def main():
    parser = argparse.ArgumentParser(
        description="Display information about Student Report Card RAG corpora"
    )
    parser.add_argument(
        "--corpus",
        help="Specific corpus name to inspect (default: configured corpus)"
    )
    parser.add_argument(
        "--list-all",
        action="store_true",
        help="List all available corpora"
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Show detailed file information"
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("📊 Student Report Card RAG - Corpus Information")
    print("="*60)
    
    if args.list_all:
        # List all corpora
        all_corpora = list_all_corpora()
        
        if all_corpora:
            print(f"\n📋 Summary: Found {len(all_corpora)} corpora in project '{PROJECT_ID}'")
            
            for corpus in all_corpora:
                print(f"\n📚 {corpus['display_name']}")
                print(f"   Resource: {corpus['name']}")
        else:
            print("\n❌ No corpora found in this project.")
            print("   Create a corpus first with: python check_corpus.py")
        
        return 0
    
    # Find target corpus
    target_corpus_name = args.corpus or RAG_CORPUS_NAME
    
    try:
        corpora = rag.list_corpora()
        target_corpus = None
        
        for corpus in corpora:
            if corpus.display_name == target_corpus_name:
                target_corpus = {
                    'display_name': corpus.display_name,
                    'name': corpus.name,
                    'corpus': corpus
                }
                break
        
        if not target_corpus:
            print(f"\n❌ Corpus '{target_corpus_name}' not found!")
            print("   Available corpora:")
            for corpus in corpora:
                print(f"     - {corpus.display_name}")
            return 1
        
        print(f"\n🎯 Inspecting corpus: {target_corpus['display_name']}")
        
        # Get file details
        file_details = get_corpus_files(target_corpus['name'])
        
        # Display statistics
        display_corpus_stats(target_corpus, file_details)
        
        # Display detailed file info if requested
        if args.detailed:
            display_detailed_files(file_details)
        
        # Summary and recommendations
        print(f"\n📋 Summary")
        print("=" * 50)
        
        if not file_details:
            print("⚠️  Corpus is empty - no documents indexed")
            print("\nNext steps:")
            print("  1. Add documents: python add_documents.py --source local --paths ./sample-data/")
            print("  2. Test queries: python query_corpus.py")
        else:
            print(f"✅ Corpus contains {len(file_details)} documents")
            print("\nNext steps:")
            print("  1. Test queries: python query_corpus.py")
            print("  2. Start building your Streamlit app")
            print("  3. Add more documents as needed")
        
    except Exception as e:
        print(f"\n❌ Error inspecting corpus: {str(e)}")
        return 1
    
    print("\n" + "="*60)
    print("📊 Corpus inspection completed!")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    exit(main()) 