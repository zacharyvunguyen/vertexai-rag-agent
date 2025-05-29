"""
Sidebar component for the RAG Corpus Manager.
Contains controls for refreshing data, uploading documents, and danger zone operations.
"""

import streamlit as st
from corpus_manager.config import SUPPORTED_FILE_TYPES


def render_sidebar():
    """Render the sidebar with controls and upload functionality."""
    with st.sidebar:
        st.markdown("### 🎛️ Controls")
        
        # Refresh button
        refresh_clicked = st.button("🔄 Refresh Data", use_container_width=True)
        
        st.markdown("---")
        
        # Upload section
        st.markdown("### 📁 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=SUPPORTED_FILE_TYPES,
            help=f"Upload {', '.join(SUPPORTED_FILE_TYPES).upper()} files to add to the corpus"
        )
        
        upload_clicked = False
        if uploaded_file:
            upload_clicked = st.button("Upload to Corpus", type="primary", use_container_width=True)
        
        st.markdown("---")
        
        # Danger zone
        st.markdown("### ⚠️ Danger Zone")
        delete_all_clicked = st.button(
            "🗑️ Delete All Documents", 
            type="secondary", 
            use_container_width=True,
            help="This will delete all documents from the corpus"
        )
        
        return {
            'refresh_clicked': refresh_clicked,
            'uploaded_file': uploaded_file,
            'upload_clicked': upload_clicked,
            'delete_all_clicked': delete_all_clicked
        } 