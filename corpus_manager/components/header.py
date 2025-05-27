"""
Header component for the RAG Corpus Manager.
Displays the main application header with title and description.
"""

import streamlit as st


def render_header():
    """Render the main application header."""
    st.markdown("""
    <div class="main-header">
        <h1>📚 RAG Corpus Manager</h1>
        <p>Manage your Student Report Card RAG corpus documents with ease</p>
    </div>
    """, unsafe_allow_html=True) 