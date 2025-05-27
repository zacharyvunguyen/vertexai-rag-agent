#!/usr/bin/env python3
"""
Student Report Card RAG System - Corpus Management App
A modern, minimalist Streamlit interface for managing RAG corpus documents.
"""

import os
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv
from vertexai import rag
import vertexai
from pathlib import Path
import tempfile

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="RAG Corpus Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, minimalist design
st.markdown("""
<style>
    /* Modern color palette */
    :root {
        --primary-blue: #2563eb;
        --light-blue: #eff6ff;
        --dark-gray: #1f2937;
        --medium-gray: #6b7280;
        --light-gray: #f9fafb;
        --success-green: #10b981;
        --warning-orange: #f59e0b;
        --danger-red: #ef4444;
        --border-radius: 12px;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    }
    
    /* Main content styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, var(--primary-blue), #3b82f6);
        padding: 2rem;
        border-radius: var(--border-radius);
        color: white;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }
    
    .main-header h1 {
        margin: 0;
        font-weight: 600;
        font-size: 2.5rem;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: var(--light-gray);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-blue);
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--medium-gray);
        margin: 0.25rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Document item styling */
    .document-item {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .document-item:hover {
        box-shadow: var(--shadow);
        border-color: var(--primary-blue);
    }
    
    .document-title {
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--dark-gray);
        margin: 0 0 0.5rem 0;
    }
    
    .document-meta {
        font-size: 0.875rem;
        color: var(--medium-gray);
        margin: 0.25rem 0;
    }
    
    .document-actions {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-success {
        background: #dcfce7;
        color: #166534;
    }
    
    .status-warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .status-error {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: var(--border-radius);
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: var(--light-gray);
    }
    
    /* Upload area styling */
    .upload-area {
        border: 2px dashed #d1d5db;
        border-radius: var(--border-radius);
        padding: 2rem;
        text-align: center;
        background: var(--light-blue);
        margin: 1rem 0;
    }
    
    /* Table styling */
    .stDataFrame {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--shadow);
    }
    
    /* Alert styling */
    .alert {
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
    }
    
    .alert-success {
        background: #dcfce7;
        border: 1px solid #bbf7d0;
        color: #166534;
    }
    
    .alert-error {
        background: #fee2e2;
        border: 1px solid #fecaca;
        color: #991b1b;
    }
    
    .alert-warning {
        background: #fef3c7;
        border: 1px solid #fed7aa;
        color: #92400e;
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background-color: var(--light-blue);
    }
    
    .stProgress .st-bp {
        background-color: var(--primary-blue);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Vertex AI
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION")
RAG_CORPUS_NAME = os.environ.get("RAG_CORPUS_NAME")

@st.cache_resource
def initialize_vertex_ai():
    """Initialize Vertex AI with caching."""
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    return True

def find_corpus() -> Optional[str]:
    """Find the corpus resource name."""
    try:
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
            chunk_size=512,
            chunk_overlap=100
        )
        
        # Clean up
        os.unlink(tmp_path)
        return True
        
    except Exception as e:
        st.error(f"Error uploading document: {str(e)}")
        return False

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    sizes = ["B", "KB", "MB", "GB"]
    size = size_bytes
    unit_index = 0
    
    while size >= 1024 and unit_index < len(sizes) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.1f} {sizes[unit_index]}"

def format_date(date_obj) -> str:
    """Format datetime object to readable string."""
    if date_obj is None:
        return "Unknown"
    
    if hasattr(date_obj, 'strftime'):
        return date_obj.strftime("%Y-%m-%d %H:%M")
    else:
        return str(date_obj)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📚 RAG Corpus Manager</h1>
        <p>Manage your Student Report Card RAG corpus documents with ease</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Vertex AI
    if not initialize_vertex_ai():
        st.error("Failed to initialize Vertex AI. Please check your configuration.")
        return
    
    # Find corpus
    corpus_resource_name = find_corpus()
    if not corpus_resource_name:
        st.error(f"Corpus '{RAG_CORPUS_NAME}' not found. Please create it first.")
        return
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### 🎛️ Controls")
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Upload section
        st.markdown("### 📁 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'txt'],
            help="Upload PDF, DOCX, or TXT files to add to the corpus"
        )
        
        if uploaded_file and st.button("Upload to Corpus", type="primary", use_container_width=True):
            with st.spinner("Uploading document..."):
                if upload_document(uploaded_file, corpus_resource_name):
                    st.success(f"Successfully uploaded '{uploaded_file.name}'!")
                    st.cache_data.clear()
                    st.rerun()
        
        st.markdown("---")
        
        # Danger zone
        st.markdown("### ⚠️ Danger Zone")
        if st.button("🗑️ Delete All Documents", 
                    type="secondary", 
                    use_container_width=True,
                    help="This will delete all documents from the corpus"):
            st.session_state.show_delete_all_modal = True
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    # Get documents
    documents = get_corpus_documents(corpus_resource_name)
    
    # Metrics
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(documents)}</div>
            <div class="metric-label">Total Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_size = sum(doc['size_bytes'] for doc in documents)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_file_size(total_size)}</div>
            <div class="metric-label">Total Size</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # File types
        file_types = {}
        for doc in documents:
            ext = doc['display_name'].lower().split('.')[-1] if '.' in doc['display_name'] else 'unknown'
            file_types[ext] = file_types.get(ext, 0) + 1
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(file_types)}</div>
            <div class="metric-label">File Types</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Latest document
        latest_doc = documents[0] if documents else None
        latest_date = format_date(latest_doc['create_time']) if latest_doc else "None"
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size: 1rem;">{latest_date}</div>
            <div class="metric-label">Latest Upload</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Document List", "📊 Analytics", "🔧 Bulk Operations"])
    
    with tab1:
        if not documents:
            st.markdown("""
            <div class="info-card" style="text-align: center; padding: 3rem;">
                <h3>📭 No Documents Found</h3>
                <p>Upload your first document using the sidebar to get started.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Search and filter
            search_col, filter_col = st.columns([3, 1])
            
            with search_col:
                search_term = st.text_input("🔍 Search documents", placeholder="Enter document name...")
            
            with filter_col:
                file_type_filter = st.selectbox(
                    "Filter by type",
                    ["All"] + list(set(doc['display_name'].lower().split('.')[-1] for doc in documents if '.' in doc['display_name']))
                )
            
            # Filter documents
            filtered_docs = documents
            if search_term:
                filtered_docs = [doc for doc in filtered_docs if search_term.lower() in doc['display_name'].lower()]
            if file_type_filter != "All":
                filtered_docs = [doc for doc in filtered_docs if doc['display_name'].lower().endswith(f".{file_type_filter}")]
            
            st.markdown(f"**Showing {len(filtered_docs)} of {len(documents)} documents**")
            
            # Document list
            for i, doc in enumerate(filtered_docs):
                with st.container():
                    st.markdown(f"""
                    <div class="document-item">
                        <div class="document-title">📄 {doc['display_name']}</div>
                        <div class="document-meta">
                            <strong>Size:</strong> {format_file_size(doc['size_bytes'])} | 
                            <strong>Created:</strong> {format_date(doc['create_time'])}
                        </div>
                        <div class="document-meta">
                            <strong>Resource ID:</strong> <code>{doc['name'].split('/')[-1]}</code>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Action buttons
                    col_info, col_delete = st.columns([3, 1])
                    
                    with col_info:
                        if st.button(f"ℹ️ View Details", key=f"info_{i}"):
                            st.session_state[f"show_details_{i}"] = not st.session_state.get(f"show_details_{i}", False)
                    
                    with col_delete:
                        if st.button(f"🗑️ Delete", key=f"delete_{i}", type="secondary"):
                            st.session_state[f"confirm_delete_{i}"] = True
                    
                    # Show details if requested
                    if st.session_state.get(f"show_details_{i}", False):
                        st.json({
                            "Display Name": doc['display_name'],
                            "Resource Name": doc['name'],
                            "Size (bytes)": doc['size_bytes'],
                            "Created": str(doc['create_time']),
                            "Updated": str(doc['update_time'])
                        })
                    
                    # Confirmation dialog for delete
                    if st.session_state.get(f"confirm_delete_{i}", False):
                        st.warning(f"⚠️ Are you sure you want to delete '{doc['display_name']}'?")
                        
                        confirm_col, cancel_col = st.columns(2)
                        
                        with confirm_col:
                            if st.button(f"✅ Yes, Delete", key=f"confirm_yes_{i}", type="primary"):
                                with st.spinner("Deleting document..."):
                                    if delete_document(doc['name'], doc['display_name']):
                                        st.success(f"Successfully deleted '{doc['display_name']}'!")
                                        st.cache_data.clear()
                                        st.rerun()
                        
                        with cancel_col:
                            if st.button(f"❌ Cancel", key=f"confirm_no_{i}"):
                                st.session_state[f"confirm_delete_{i}"] = False
                                st.rerun()
    
    with tab2:
        if documents:
            # File type distribution
            st.markdown("### 📊 File Type Distribution")
            
            file_type_data = {}
            for doc in documents:
                ext = doc['display_name'].lower().split('.')[-1] if '.' in doc['display_name'] else 'unknown'
                file_type_data[ext] = file_type_data.get(ext, 0) + 1
            
            df_types = pd.DataFrame(list(file_type_data.items()), columns=['File Type', 'Count'])
            st.bar_chart(df_types.set_index('File Type'))
            
            # Size distribution
            st.markdown("### 📈 Document Sizes")
            
            size_data = []
            for doc in documents:
                size_data.append({
                    'Document': doc['display_name'][:30] + '...' if len(doc['display_name']) > 30 else doc['display_name'],
                    'Size (MB)': doc['size_bytes'] / (1024 * 1024) if doc['size_bytes'] > 0 else 0
                })
            
            if size_data:
                df_sizes = pd.DataFrame(size_data)
                st.bar_chart(df_sizes.set_index('Document'))
            
            # Upload timeline
            st.markdown("### 📅 Upload Timeline")
            
            timeline_data = []
            for doc in documents:
                if doc['create_time']:
                    date = doc['create_time'].date() if hasattr(doc['create_time'], 'date') else doc['create_time']
                    timeline_data.append({'Date': date, 'Documents': 1})
            
            if timeline_data:
                df_timeline = pd.DataFrame(timeline_data)
                df_timeline = df_timeline.groupby('Date').sum().reset_index()
                st.line_chart(df_timeline.set_index('Date'))
        else:
            st.info("No data available for analytics. Upload some documents first!")
    
    with tab3:
        st.markdown("### 🔧 Bulk Operations")
        
        if documents:
            # Select documents for bulk operations
            st.markdown("#### Select Documents")
            
            selected_docs = []
            select_all = st.checkbox("Select All Documents")
            
            if select_all:
                selected_docs = list(range(len(documents)))
            else:
                for i, doc in enumerate(documents):
                    if st.checkbox(f"{doc['display_name']}", key=f"bulk_select_{i}"):
                        selected_docs.append(i)
            
            if selected_docs:
                st.markdown(f"**Selected {len(selected_docs)} documents**")
                
                # Bulk delete
                if st.button("🗑️ Delete Selected Documents", type="secondary"):
                    st.session_state.show_bulk_delete_modal = True
            else:
                st.info("Select documents to perform bulk operations.")
        else:
            st.info("No documents available for bulk operations.")
    
    # Delete all modal
    if st.session_state.get('show_delete_all_modal', False):
        with st.container():
            st.markdown("""
            <div class="alert alert-error">
                <h4>⚠️ Delete All Documents</h4>
                <p>This action will permanently delete ALL documents from the corpus. This cannot be undone.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Yes, Delete All", type="primary"):
                    with st.spinner("Deleting all documents..."):
                        deleted_count = 0
                        for doc in documents:
                            if delete_document(doc['name'], doc['display_name']):
                                deleted_count += 1
                        
                        if deleted_count == len(documents):
                            st.success(f"Successfully deleted all {deleted_count} documents!")
                        else:
                            st.warning(f"Deleted {deleted_count} of {len(documents)} documents.")
                        
                        st.session_state.show_delete_all_modal = False
                        st.cache_data.clear()
                        st.rerun()
            
            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.show_delete_all_modal = False
                    st.rerun()
    
    # Bulk delete modal
    if st.session_state.get('show_bulk_delete_modal', False):
        with st.container():
            st.markdown("""
            <div class="alert alert-warning">
                <h4>⚠️ Delete Selected Documents</h4>
                <p>This action will permanently delete the selected documents. This cannot be undone.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Yes, Delete Selected", type="primary"):
                    with st.spinner("Deleting selected documents..."):
                        deleted_count = 0
                        for i in selected_docs:
                            doc = documents[i]
                            if delete_document(doc['name'], doc['display_name']):
                                deleted_count += 1
                        
                        st.success(f"Successfully deleted {deleted_count} documents!")
                        st.session_state.show_bulk_delete_modal = False
                        st.cache_data.clear()
                        st.rerun()
            
            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.show_bulk_delete_modal = False
                    st.rerun()

if __name__ == "__main__":
    main() 