"""
Document list page for the RAG Corpus Manager.
Displays all documents in the corpus with search and delete functionality.
"""

import streamlit as st
from typing import List, Dict
from corpus_manager.utils.formatters import format_file_size, format_date, format_resource_id
from corpus_manager.utils.vertex_ai import delete_document


def render_document_list(documents: List[Dict]):
    """Render the document list page with search and filter functionality."""
    if not documents:
        st.markdown("""
        <div class="info-card" style="text-align: center; padding: 3rem;">
            <h3>📭 No Documents Found</h3>
            <p>Upload your first document using the sidebar to get started.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Search and filter controls
    search_col, filter_col = st.columns([3, 1])
    
    with search_col:
        search_term = st.text_input("🔍 Search documents", placeholder="Enter document name...")
    
    with filter_col:
        # Get unique file types
        file_types = set()
        for doc in documents:
            if '.' in doc['display_name']:
                ext = doc['display_name'].lower().split('.')[-1]
                file_types.add(ext)
        
        file_type_filter = st.selectbox(
            "Filter by type",
            ["All"] + sorted(list(file_types))
        )
    
    # Filter documents based on search and filter
    filtered_docs = documents
    if search_term:
        filtered_docs = [
            doc for doc in filtered_docs 
            if search_term.lower() in doc['display_name'].lower()
        ]
    if file_type_filter != "All":
        filtered_docs = [
            doc for doc in filtered_docs 
            if doc['display_name'].lower().endswith(f".{file_type_filter}")
        ]
    
    # Show results count
    st.markdown(f"**Showing {len(filtered_docs)} of {len(documents)} documents**")
    
    # Document list
    for i, doc in enumerate(filtered_docs):
        _render_document_item(doc, i)


def _render_document_item(doc: Dict, index: int):
    """Render an individual document item with actions."""
    with st.container():
        # Document info card
        st.markdown(f"""
        <div class="document-item">
            <div class="document-title">📄 {doc['display_name']}</div>
            <div class="document-meta">
                <strong>Size:</strong> {format_file_size(doc['size_bytes'])} | 
                <strong>Created:</strong> {format_date(doc['create_time'])}
            </div>
            <div class="document-meta">
                <strong>Resource ID:</strong> <code>{format_resource_id(doc['name'])}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col_info, col_delete = st.columns([3, 1])
        
        with col_info:
            if st.button(f"ℹ️ View Details", key=f"info_{index}"):
                st.session_state[f"show_details_{index}"] = not st.session_state.get(f"show_details_{index}", False)
        
        with col_delete:
            if st.button(f"🗑️ Delete", key=f"delete_{index}", type="secondary"):
                st.session_state[f"confirm_delete_{index}"] = True
        
        # Show details if requested
        if st.session_state.get(f"show_details_{index}", False):
            st.json({
                "Display Name": doc['display_name'],
                "Resource Name": doc['name'],
                "Size (bytes)": doc['size_bytes'],
                "Created": str(doc['create_time']),
                "Updated": str(doc['update_time'])
            })
        
        # Confirmation dialog for delete
        if st.session_state.get(f"confirm_delete_{index}", False):
            _render_delete_confirmation(doc, index)


def _render_delete_confirmation(doc: Dict, index: int):
    """Render delete confirmation dialog for a document."""
    st.warning(f"⚠️ Are you sure you want to delete '{doc['display_name']}'?")
    
    confirm_col, cancel_col = st.columns(2)
    
    with confirm_col:
        if st.button(f"✅ Yes, Delete", key=f"confirm_yes_{index}", type="primary"):
            with st.spinner("Deleting document..."):
                if delete_document(doc['name'], doc['display_name']):
                    st.success(f"Successfully deleted '{doc['display_name']}'!")
                    # Clear cache and rerun
                    st.cache_data.clear()
                    # Clear the confirmation state
                    st.session_state[f"confirm_delete_{index}"] = False
                    st.rerun()
    
    with cancel_col:
        if st.button(f"❌ Cancel", key=f"confirm_no_{index}"):
            st.session_state[f"confirm_delete_{index}"] = False
            st.rerun() 