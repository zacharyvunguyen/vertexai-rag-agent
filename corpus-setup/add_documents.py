#!/usr/bin/env python3
"""
Script to add documents to the Student Report Card RAG corpus.
Supports adding from local files, Google Cloud Storage, and Google Drive.
"""

import os
import sys
import argparse
import glob
from pathlib import Path
from dotenv import load_dotenv
from vertexai import rag
import vertexai

# Load environment variables
load_dotenv()

# Initialize Vertex AI
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION")
RAG_CORPUS_NAME = os.environ.get("RAG_CORPUS_NAME")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

print(f"Initializing Vertex AI with project={PROJECT_ID}, location={LOCATION}")
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Supported file types
SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.doc'}

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

def upload_to_gcs(local_path, gcs_path):
    """Upload local file to Google Cloud Storage."""
    try:
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(gcs_path)
        
        blob.upload_from_filename(local_path)
        print(f"   ✅ Uploaded {local_path} to gs://{BUCKET_NAME}/{gcs_path}")
        return f"gs://{BUCKET_NAME}/{gcs_path}"
    except Exception as e:
        print(f"   ❌ Error uploading {local_path}: {str(e)}")
        return None

def add_local_files(file_paths):
    """Add local files to the corpus by uploading to GCS first."""
    print(f"\n📁 Processing {len(file_paths)} local files...")
    
    gcs_paths = []
    for file_path in file_paths:
        file_path = Path(file_path)
        
        # Check if file exists and has supported extension
        if not file_path.exists():
            print(f"   ⚠️  File not found: {file_path}")
            continue
            
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            print(f"   ⚠️  Unsupported file type: {file_path}")
            continue
        
        # Upload to GCS in processing folder
        gcs_path = f"processing/{file_path.name}"
        gcs_url = upload_to_gcs(str(file_path), gcs_path)
        
        if gcs_url:
            gcs_paths.append(gcs_url)
    
    return gcs_paths

def add_gcs_paths(paths):
    """Process GCS paths for adding to corpus."""
    print(f"\n☁️  Processing {len(paths)} GCS paths...")
    
    processed_paths = []
    for path in paths:
        if path.startswith('gs://'):
            processed_paths.append(path)
            print(f"   ✅ Added GCS path: {path}")
        else:
            print(f"   ⚠️  Invalid GCS path: {path}")
    
    return processed_paths

def add_to_corpus(paths):
    """Add documents to the RAG corpus."""
    if not paths:
        print("   ⚠️  No valid paths to add to corpus")
        return False
    
    try:
        # Get corpus resource name
        corpus_resource_name = get_corpus_resource_name()
        if not corpus_resource_name:
            print(f"   ❌ Corpus '{RAG_CORPUS_NAME}' not found. Please create it first.")
            return False
        
        print(f"\n📚 Adding {len(paths)} documents to corpus...")
        print(f"   Corpus: {RAG_CORPUS_NAME}")
        
        # Configure chunking
        transformation_config = rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(
                chunk_size=512,
                chunk_overlap=100,
            ),
        )
        
        # Import files to corpus
        import_result = rag.import_files(
            corpus_resource_name,
            paths,
            transformation_config=transformation_config,
            max_embedding_requests_per_min=1000,
        )
        
        print(f"   ✅ Successfully added {import_result.imported_rag_files_count} files to corpus!")
        print(f"   Chunk size: 512 tokens")
        print(f"   Chunk overlap: 100 tokens")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error adding documents to corpus: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Add documents to the Student Report Card RAG corpus"
    )
    parser.add_argument(
        "--source",
        choices=["local", "gcs"],
        required=True,
        help="Source type: local files or GCS paths"
    )
    parser.add_argument(
        "--paths",
        nargs="+",
        required=True,
        help="File paths or GCS URLs to add"
    )
    parser.add_argument(
        "--pattern",
        help="Glob pattern for local files (e.g., '*.pdf')"
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("📚 Student Report Card RAG - Add Documents")
    print("="*60)
    
    # Expand paths if pattern is provided
    if args.source == "local" and args.pattern:
        expanded_paths = []
        for base_path in args.paths:
            pattern_path = os.path.join(base_path, args.pattern)
            expanded_paths.extend(glob.glob(pattern_path))
        args.paths = expanded_paths
    
    # Process paths based on source type
    if args.source == "local":
        gcs_paths = add_local_files(args.paths)
        if gcs_paths and add_to_corpus(gcs_paths):
            print(f"\n🎉 Successfully processed {len(gcs_paths)} local files!")
        else:
            print(f"\n❌ Failed to process local files")
            return 1
            
    elif args.source == "gcs":
        gcs_paths = add_gcs_paths(args.paths)
        if gcs_paths and add_to_corpus(gcs_paths):
            print(f"\n🎉 Successfully processed {len(gcs_paths)} GCS files!")
        else:
            print(f"\n❌ Failed to process GCS files")
            return 1
    
    print("\n" + "="*60)
    print("📋 Next Steps:")
    print("   1. Test queries with: python query_corpus.py")
    print("   2. Check corpus info: python corpus_info.py")
    print("   3. Start building your Streamlit app")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    exit(main()) 