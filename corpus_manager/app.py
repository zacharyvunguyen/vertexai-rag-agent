#!/usr/bin/env python3
"""
Main Streamlit application for the RAG Corpus Manager.
A modern, minimalist interface for managing RAG corpus documents.
"""

import streamlit as st

# Import configuration and validation
from .config import PAGE_TITLE, PAGE_ICON, LAYOUT, validate_config

# Import components
from .components.styles import apply_custom_css
from .components.header import render_header
from .components.metrics import render_metrics
from .components.sidebar import render_sidebar

# Import pages
from .pages.document_list import render_document_list
from .pages.analytics import render_analytics
from .pages.bulk_operations import render_bulk_operations

# Import utilities
from .utils.vertex_ai import initialize_vertex_ai, find_corpus, get_corpus_documents, upload_document, bulk_delete_documents


def main():
    """Main application function."""
    
    # Configure Streamlit page
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS styles
    apply_custom_css()
    
    # Validate configuration
    try:
        validate_config()
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.stop()
    
    # Render header
    render_header()
    
    # Initialize Vertex AI
    if not initialize_vertex_ai():
        st.error("Failed to initialize Vertex AI. Please check your configuration.")
        st.stop()
    
    # Find corpus
    corpus_resource_name = find_corpus()
    if not corpus_resource_name:
        st.error("Corpus not found. Please create it first using the setup scripts.")
        st.stop()
    
    # Render sidebar and get user actions
    sidebar_actions = render_sidebar()
    
    # Handle sidebar actions
    _handle_sidebar_actions(sidebar_actions, corpus_resource_name)
    
    # Get documents from corpus
    documents = get_corpus_documents(corpus_resource_name)
    
    # Render metrics
    render_metrics(documents)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Document List", "📊 Analytics", "🔧 Bulk Operations"])
    
    with tab1:
        render_document_list(documents)
    
    with tab2:
        render_analytics(documents)
    
    with tab3:
        render_bulk_operations(documents)
    
    # Handle delete all modal
    _handle_delete_all_modal(documents)


def _handle_sidebar_actions(actions: dict, corpus_resource_name: str):
    """Handle actions from the sidebar."""
    
    # Handle refresh
    if actions['refresh_clicked']:
        st.cache_data.clear()
        st.rerun()
    
    # Handle upload
    if actions['upload_clicked'] and actions['uploaded_file']:
        with st.spinner("Uploading document..."):
            if upload_document(actions['uploaded_file'], corpus_resource_name):
                st.success(f"Successfully uploaded '{actions['uploaded_file'].name}'!")
                st.cache_data.clear()
                st.rerun()
    
    # Handle delete all
    if actions['delete_all_clicked']:
        st.session_state.show_delete_all_modal = True


def _handle_delete_all_modal(documents: list):
    """Handle the delete all documents modal."""
    if st.session_state.get('show_delete_all_modal', False):
        st.markdown("---")
        
        # Warning message
        st.markdown("""
        <div class="alert alert-error">
            <h4>⚠️ Delete All Documents</h4>
            <p>This action will permanently delete ALL documents from the corpus. This cannot be undone.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show document count
        st.warning(f"This will delete **{len(documents)} documents** from the corpus.")
        
        # Confirmation buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Yes, Delete All", type="primary", key="confirm_delete_all"):
                with st.spinner("Deleting all documents..."):
                    # Prepare document info for deletion
                    doc_names = [doc['name'] for doc in documents]
                    display_names = [doc['display_name'] for doc in documents]
                    
                    # Perform bulk deletion
                    result = bulk_delete_documents(doc_names, display_names)
                    
                    # Show results
                    if result['deleted'] == result['total']:
                        st.success(f"✅ Successfully deleted all {result['deleted']} documents!")
                    elif result['deleted'] > 0:
                        st.warning(f"⚠️ Deleted {result['deleted']} of {result['total']} documents. {result['failed']} failed.")
                    else:
                        st.error(f"❌ Failed to delete any documents. {result['failed']} failed.")
                    
                    # Clear the modal and cache
                    st.session_state.show_delete_all_modal = False
                    st.cache_data.clear()
                    st.rerun()
        
        with col2:
            if st.button("❌ Cancel", key="cancel_delete_all"):
                st.session_state.show_delete_all_modal = False
                st.rerun()


if __name__ == "__main__":
    main() 