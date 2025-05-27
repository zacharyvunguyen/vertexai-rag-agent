"""
Bulk operations page for the RAG Corpus Manager.
Allows users to select multiple documents and perform bulk operations like deletion.
"""

import streamlit as st
from typing import List, Dict
from ..utils.vertex_ai import bulk_delete_documents


def render_bulk_operations(documents: List[Dict]):
    """Render the bulk operations page."""
    st.markdown("### 🔧 Bulk Operations")
    
    if not documents:
        st.info("No documents available for bulk operations.")
        return
    
    # Document selection
    st.markdown("#### Select Documents")
    
    # Select all checkbox
    select_all = st.checkbox("Select All Documents")
    
    selected_docs = []
    
    if select_all:
        selected_docs = list(range(len(documents)))
        st.info(f"All {len(documents)} documents selected")
    else:
        # Individual selection
        with st.container():
            # Create columns for better layout
            cols_per_row = 2
            for i in range(0, len(documents), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    doc_index = i + j
                    if doc_index < len(documents):
                        doc = documents[doc_index]
                        with cols[j]:
                            if st.checkbox(f"{doc['display_name']}", key=f"bulk_select_{doc_index}"):
                                selected_docs.append(doc_index)
    
    # Show selection summary
    if selected_docs:
        st.markdown(f"**Selected {len(selected_docs)} documents**")
        
        # Calculate total size of selected documents
        total_size = sum(documents[i]['size_bytes'] for i in selected_docs)
        size_mb = total_size / (1024 * 1024) if total_size > 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Selected Documents", len(selected_docs))
        with col2:
            st.metric("Total Size", f"{size_mb:.1f} MB")
        
        # Show selected documents list
        with st.expander("📋 View selected documents"):
            for i in selected_docs:
                doc = documents[i]
                st.write(f"• {doc['display_name']}")
        
        st.markdown("---")
        
        # Bulk operations
        st.markdown("#### Available Operations")
        
        # Bulk delete
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("🗑️ Delete Selected", type="secondary", use_container_width=True):
                st.session_state.show_bulk_delete_modal = True
        
        with col2:
            st.write("Permanently delete all selected documents from the corpus")
        
        # Bulk delete confirmation modal
        if st.session_state.get('show_bulk_delete_modal', False):
            _render_bulk_delete_modal(documents, selected_docs)
            
    else:
        st.info("Select documents to perform bulk operations.")


def _render_bulk_delete_modal(documents: List[Dict], selected_indices: List[int]):
    """Render the bulk delete confirmation modal."""
    st.markdown("---")
    
    # Warning message
    st.markdown("""
    <div class="alert alert-warning">
        <h4>⚠️ Delete Selected Documents</h4>
        <p>This action will permanently delete the selected documents from the corpus. This cannot be undone.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show documents to be deleted
    with st.expander("📋 Documents to be deleted"):
        for i in selected_indices:
            doc = documents[i]
            st.write(f"• {doc['display_name']}")
    
    # Confirmation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Yes, Delete Selected", type="primary", key="confirm_bulk_delete"):
            with st.spinner("Deleting selected documents..."):
                # Prepare document info for deletion
                doc_names = [documents[i]['name'] for i in selected_indices]
                display_names = [documents[i]['display_name'] for i in selected_indices]
                
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
                st.session_state.show_bulk_delete_modal = False
                st.cache_data.clear()
                st.rerun()
    
    with col2:
        if st.button("❌ Cancel", key="cancel_bulk_delete"):
            st.session_state.show_bulk_delete_modal = False
            st.rerun() 