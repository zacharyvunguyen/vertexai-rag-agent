"""
Vertex AI utilities for the RAG Corpus Manager.
Handles corpus operations and document management.
"""

import os
import streamlit as st
from typing import List, Dict, Optional, Tuple
import json
import time
import tempfile
from datetime import datetime
from io import BytesIO

import vertexai
from vertexai.preview import rag
from google.cloud import aiplatform

from corpus_manager.config import PROJECT_ID, LOCATION, RAG_CORPUS_NAME, UPLOAD_CHUNK_SIZE, UPLOAD_CHUNK_OVERLAP


@st.cache_resource
def initialize_vertex_ai():
    """Initialize Vertex AI with caching."""
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        return True
    except Exception as e:
        st.error(f"Failed to initialize Vertex AI: {str(e)}")
        return False


def find_corpus() -> Optional[str]:
    """Find the corpus resource name."""
    try:
        # If RAG_CORPUS_NAME is already a full path (starts with 'projects/'), use it directly
        if RAG_CORPUS_NAME and RAG_CORPUS_NAME.startswith('projects/'):
            return RAG_CORPUS_NAME
        
        # Otherwise, try to find by display name
        corpora = rag.list_corpora()
        for corpus in corpora:
            if corpus.display_name == RAG_CORPUS_NAME:
                return corpus.name
        return None
    except Exception as e:
        st.error(f"Error finding corpus: {str(e)}")
        return None


@st.cache_data(ttl=60)
def get_corpus_documents(corpus_resource_name: str) -> List[Dict]:
    """Get list of documents in the corpus with caching."""
    try:
        files = rag.list_files(corpus_name=corpus_resource_name)
        documents = []
        
        for file in files:
            doc_info = {
                'name': getattr(file, 'name', 'Unknown'),
                'display_name': getattr(file, 'display_name', 'Unknown'),
                'size_bytes': getattr(file, 'size_bytes', 0),
                'create_time': getattr(file, 'create_time', None),
                'update_time': getattr(file, 'update_time', None),
            }
            documents.append(doc_info)
        
        # Sort by creation time (newest first)
        documents.sort(key=lambda x: x['create_time'] or datetime.min, reverse=True)
        return documents
    
    except Exception as e:
        st.error(f"Error retrieving documents: {str(e)}")
        return []


def delete_document(document_name: str, display_name: str) -> bool:
    """Delete a document from the corpus."""
    try:
        rag.delete_file(name=document_name)
        return True
    except Exception as e:
        st.error(f"Error deleting document '{display_name}': {str(e)}")
        return False


def upload_document(uploaded_file, corpus_resource_name: str) -> bool:
    """Upload a document to the corpus."""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        
        # Import to corpus
        rag.import_files(
            corpus_name=corpus_resource_name,
            paths=[tmp_path],
            chunk_size=UPLOAD_CHUNK_SIZE,
            chunk_overlap=UPLOAD_CHUNK_OVERLAP
        )
        
        # Clean up
        os.unlink(tmp_path)
        return True
        
    except Exception as e:
        st.error(f"Error uploading document: {str(e)}")
        return False


def get_corpus_stats(documents: List[Dict]) -> Dict:
    """Calculate corpus statistics."""
    if not documents:
        return {
            'total_documents': 0,
            'total_size': 0,
            'file_types': {},
            'latest_upload': None
        }
    
    # Calculate total size
    total_size = sum(doc['size_bytes'] for doc in documents)
    
    # Calculate file types
    file_types = {}
    for doc in documents:
        ext = doc['display_name'].lower().split('.')[-1] if '.' in doc['display_name'] else 'unknown'
        file_types[ext] = file_types.get(ext, 0) + 1
    
    # Find latest upload
    latest_doc = documents[0] if documents else None
    latest_upload = latest_doc['create_time'] if latest_doc else None
    
    return {
        'total_documents': len(documents),
        'total_size': total_size,
        'file_types': file_types,
        'latest_upload': latest_upload
    }


def bulk_delete_documents(document_names: List[str], display_names: List[str]) -> Dict[str, int]:
    """Delete multiple documents from the corpus."""
    deleted_count = 0
    failed_count = 0
    
    for doc_name, display_name in zip(document_names, display_names):
        try:
            rag.delete_file(name=doc_name)
            deleted_count += 1
        except Exception as e:
            st.error(f"Failed to delete {display_name}: {str(e)}")
            failed_count += 1
    
    return {
        'deleted': deleted_count,
        'failed': failed_count,
        'total': len(document_names)
    } 