"""
Metrics component for the RAG Corpus Manager.
Displays key corpus statistics and metrics.
"""

import streamlit as st
from typing import List, Dict
from corpus_manager.utils.formatters import format_file_size, format_date


def render_metrics(documents: List[Dict]):
    """Render corpus metrics in a card layout."""
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics
    total_documents = len(documents)
    total_size = sum(doc['size_bytes'] for doc in documents)
    
    # File types
    file_types = {}
    for doc in documents:
        ext = doc['display_name'].lower().split('.')[-1] if '.' in doc['display_name'] else 'unknown'
        file_types[ext] = file_types.get(ext, 0) + 1
    
    # Latest document
    latest_doc = documents[0] if documents else None
    latest_date = format_date(latest_doc['create_time']) if latest_doc else "None"
    
    # Render metric cards
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_documents}</div>
            <div class="metric-label">Total Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_file_size(total_size)}</div>
            <div class="metric-label">Total Size</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(file_types)}</div>
            <div class="metric-label">File Types</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Adjust font size for date to fit better
        font_size = "1rem" if len(latest_date) > 12 else "1.2rem"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size: {font_size};">{latest_date}</div>
            <div class="metric-label">Latest Upload</div>
        </div>
        """, unsafe_allow_html=True) 