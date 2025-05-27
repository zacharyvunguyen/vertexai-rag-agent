#!/usr/bin/env python3
"""
Student Report Card RAG System - Document Management
Manage documents in the RAG corpus: list, view details, and delete documents.
"""

import os
import argparse
import sys
from typing import List, Dict, Optional
from dotenv import load_dotenv
from vertexai import rag
import vertexai

# Load environment variables
load_dotenv()

# Initialize Vertex AI
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION")
RAG_CORPUS_NAME = os.environ.get("RAG_CORPUS_NAME")

def initialize_vertex_ai():
    """Initialize Vertex AI with project configuration."""
    print(f"Initializing Vertex AI with project={PROJECT_ID}, location={LOCATION}")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

def find_corpus(corpus_name: str = None) -> Optional[str]:
    """Find the corpus resource name."""
    try:
        target_name = corpus_name or RAG_CORPUS_NAME
        corpora = rag.list_corpora()
        
        for corpus in corpora:
            if corpus.display_name == target_name:
                return corpus.name
        
        print(f"❌ Corpus '{target_name}' not found")
        return None
    
    except Exception as e:
        print(f"❌ Error finding corpus: {str(e)}")
        return None

def list_documents(corpus_resource_name: str) -> List[Dict]:
    """List all documents in the corpus."""
    try:
        print(f"\n📁 Retrieving documents from corpus...")
        
        files = rag.list_files(corpus_name=corpus_resource_name)
        file_list = list(files)
        
        if not file_list:
            print("   No documents found in corpus.")
            return []
        
        documents = []
        print(f"   Found {len(file_list)} documents:")
        
        for i, file in enumerate(file_list, 1):
            doc_info = {
                'index': i,
                'name': getattr(file, 'name', 'Unknown'),
                'display_name': getattr(file, 'display_name', 'Unknown'),
                'size_bytes': getattr(file, 'size_bytes', 0),
                'create_time': getattr(file, 'create_time', None),
                'update_time': getattr(file, 'update_time', None),
                'file_object': file
            }
            documents.append(doc_info)
            
            # Display document info
            print(f"\n   📄 [{i}] {doc_info['display_name']}")
            print(f"       Resource: {doc_info['name']}")
            
            if doc_info['size_bytes'] > 0:
                size_mb = doc_info['size_bytes'] / (1024 * 1024)
                print(f"       Size: {size_mb:.2f} MB")
            
            if doc_info['create_time']:
                print(f"       Created: {doc_info['create_time']}")
        
        return documents
    
    except Exception as e:
        print(f"❌ Error listing documents: {str(e)}")
        return []

def display_document_details(document: Dict):
    """Display detailed information about a document."""
    print(f"\n📄 Document Details")
    print("=" * 60)
    print(f"Display Name: {document['display_name']}")
    print(f"Resource Name: {document['name']}")
    
    if document['size_bytes'] > 0:
        size_mb = document['size_bytes'] / (1024 * 1024)
        print(f"Size: {document['size_bytes']:,} bytes ({size_mb:.2f} MB)")
    
    if document['create_time']:
        print(f"Created: {document['create_time']}")
    
    if document['update_time']:
        print(f"Updated: {document['update_time']}")
    
    print("=" * 60)

def delete_document(corpus_resource_name: str, document: Dict) -> bool:
    """Delete a specific document from the corpus."""
    try:
        print(f"\n🗑️  Deleting document: {document['display_name']}")
        
        # Confirm deletion
        confirm = input(f"⚠️  Are you sure you want to delete '{document['display_name']}'? (y/N): ")
        if confirm.lower() != 'y':
            print("   Deletion cancelled.")
            return False
        
        # Delete the file from the corpus
        rag.delete_file(name=document['name'])
        
        print(f"✅ Successfully deleted: {document['display_name']}")
        return True
    
    except Exception as e:
        print(f"❌ Error deleting document: {str(e)}")
        return False

def delete_all_documents(corpus_resource_name: str, documents: List[Dict]) -> bool:
    """Delete all documents from the corpus."""
    try:
        if not documents:
            print("   No documents to delete.")
            return True
        
        print(f"\n🗑️  Preparing to delete ALL {len(documents)} documents from corpus")
        print("   Documents to be deleted:")
        for doc in documents:
            print(f"   - {doc['display_name']}")
        
        # Double confirmation for bulk delete
        confirm1 = input(f"\n⚠️  Are you sure you want to delete ALL {len(documents)} documents? (y/N): ")
        if confirm1.lower() != 'y':
            print("   Bulk deletion cancelled.")
            return False
        
        confirm2 = input("⚠️  This action cannot be undone. Type 'DELETE ALL' to confirm: ")
        if confirm2 != 'DELETE ALL':
            print("   Bulk deletion cancelled.")
            return False
        
        # Delete all documents
        deleted_count = 0
        failed_count = 0
        
        for doc in documents:
            try:
                rag.delete_file(name=doc['name'])
                print(f"   ✅ Deleted: {doc['display_name']}")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ Failed to delete {doc['display_name']}: {str(e)}")
                failed_count += 1
        
        print(f"\n📊 Deletion Summary:")
        print(f"   ✅ Successfully deleted: {deleted_count}")
        if failed_count > 0:
            print(f"   ❌ Failed to delete: {failed_count}")
        
        return failed_count == 0
    
    except Exception as e:
        print(f"❌ Error during bulk deletion: {str(e)}")
        return False

def interactive_document_management(corpus_resource_name: str):
    """Interactive document management interface."""
    while True:
        print("\n" + "="*60)
        print("📚 Student Report Card RAG - Document Management")
        print("="*60)
        
        # List documents
        documents = list_documents(corpus_resource_name)
        
        if not documents:
            print("\n   No documents found. Add documents with: python add_documents.py")
            break
        
        # Display options
        print(f"\n📋 Management Options:")
        print("   [1-{}] View details for document".format(len(documents)))
        print("   [d1-d{}] Delete specific document".format(len(documents)))
        print("   [dall] Delete ALL documents")
        print("   [r] Refresh document list")
        print("   [q] Quit")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print("Exiting document management.")
            break
        elif choice == 'r':
            continue
        elif choice == 'dall':
            success = delete_all_documents(corpus_resource_name, documents)
            if success:
                print("\n✅ All documents deleted successfully.")
            else:
                print("\n❌ Some documents could not be deleted.")
        elif choice.startswith('d') and len(choice) > 1:
            # Delete specific document
            try:
                index = int(choice[1:]) - 1
                if 0 <= index < len(documents):
                    success = delete_document(corpus_resource_name, documents[index])
                    if success:
                        print(f"✅ Document deleted successfully.")
                else:
                    print("❌ Invalid document number.")
            except ValueError:
                print("❌ Invalid input. Use format 'd1', 'd2', etc.")
        elif choice.isdigit():
            # View document details
            try:
                index = int(choice) - 1
                if 0 <= index < len(documents):
                    display_document_details(documents[index])
                else:
                    print("❌ Invalid document number.")
            except ValueError:
                print("❌ Invalid input.")
        else:
            print("❌ Invalid choice. Please try again.")

def main():
    parser = argparse.ArgumentParser(
        description="Manage documents in the Student Report Card RAG corpus"
    )
    parser.add_argument(
        "--corpus",
        help="Specific corpus name (default: configured corpus)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all documents and exit"
    )
    parser.add_argument(
        "--delete",
        type=int,
        metavar="INDEX",
        help="Delete document by index number"
    )
    parser.add_argument(
        "--delete-all",
        action="store_true",
        help="Delete all documents from corpus"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive document management mode (default)"
    )
    
    args = parser.parse_args()
    
    # Initialize
    initialize_vertex_ai()
    
    # Find corpus
    corpus_resource_name = find_corpus(args.corpus)
    if not corpus_resource_name:
        sys.exit(1)
    
    print(f"Using corpus: {args.corpus or RAG_CORPUS_NAME}")
    
    # Execute based on arguments
    if args.list:
        documents = list_documents(corpus_resource_name)
        if documents:
            print(f"\n📊 Summary: Found {len(documents)} documents")
        
    elif args.delete is not None:
        documents = list_documents(corpus_resource_name)
        if documents and 1 <= args.delete <= len(documents):
            document = documents[args.delete - 1]
            success = delete_document(corpus_resource_name, document)
            sys.exit(0 if success else 1)
        else:
            print(f"❌ Invalid document index. Valid range: 1-{len(documents)}")
            sys.exit(1)
    
    elif args.delete_all:
        documents = list_documents(corpus_resource_name)
        success = delete_all_documents(corpus_resource_name, documents)
        sys.exit(0 if success else 1)
    
    else:
        # Default: interactive mode
        interactive_document_management(corpus_resource_name)

if __name__ == "__main__":
    main() 