#!/usr/bin/env python3
"""
Script to check for existing RAG corpora and create the student report card corpus if needed.
"""

import os
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

def list_existing_corpora():
    """List all existing RAG corpora."""
    try:
        print("\n🔍 Checking for existing RAG corpora...")
        corpora = rag.list_corpora()
        
        corpora_list = list(corpora)
        if not corpora_list:
            print("   No existing corpora found.")
            return []
        
        print(f"   Found {len(corpora_list)} existing corpora:")
        corpus_info = []
        for corpus in corpora_list:
            print(f"   - Display Name: {corpus.display_name}")
            print(f"     Resource Name: {corpus.name}")
            corpus_info.append({
                'display_name': corpus.display_name,
                'name': corpus.name
            })
        
        return corpus_info
        
    except Exception as e:
        print(f"   Error listing corpora: {str(e)}")
        return []

def create_student_corpus():
    """Create the student report card RAG corpus."""
    try:
        print(f"\n📚 Creating corpus: {RAG_CORPUS_NAME}")
        
        # Configure embedding model
        embedding_model_config = rag.RagEmbeddingModelConfig(
            vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                publisher_model="publishers/google/models/text-embedding-005"
            )
        )
        
        # Create the corpus
        rag_corpus = rag.create_corpus(
            display_name=RAG_CORPUS_NAME,
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=embedding_model_config
            ),
        )
        
        print(f"   ✅ Successfully created corpus!")
        print(f"   Display Name: {rag_corpus.display_name}")
        print(f"   Resource Name: {rag_corpus.name}")
        print(f"   Embedding Model: text-embedding-005")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating corpus: {str(e)}")
        return False

def main():
    print("="*60)
    print("🎓 Student Report Card RAG System - Corpus Setup")
    print("="*60)
    
    # List existing corpora
    existing_corpora = list_existing_corpora()
    
    # Check if our target corpus already exists
    corpus_exists = any(
        corpus['display_name'] == RAG_CORPUS_NAME 
        for corpus in existing_corpora
    )
    
    if corpus_exists:
        print(f"\n✅ Corpus '{RAG_CORPUS_NAME}' already exists!")
        print("   Your RAG corpus is ready for use.")
    else:
        print(f"\n📝 Corpus '{RAG_CORPUS_NAME}' not found. Creating it now...")
        
        if create_student_corpus():
            print(f"\n🎉 Corpus setup completed successfully!")
            print(f"   Your '{RAG_CORPUS_NAME}' corpus is ready for documents.")
        else:
            print(f"\n❌ Failed to create corpus. Please check the error messages above.")
            return 1
    
    print("\n" + "="*60)
    print("📋 Next Steps:")
    print("   1. Upload student report cards to your document bucket")
    print("   2. Use the add_data tool to index documents in the corpus")
    print("   3. Start querying with natural language questions")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    exit(main()) 