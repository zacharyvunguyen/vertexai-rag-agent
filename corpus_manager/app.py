#!/usr/bin/env python3
"""
Modern RAG Corpus Manager with Enhanced UI Components
Built with the latest Streamlit components for a standout experience.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
import json

# Enhanced Streamlit Components
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stateful_button import button as stateful_button

# Use absolute imports to avoid module loading issues
from corpus_manager.config import PAGE_TITLE, PAGE_ICON, LAYOUT, validate_config, SUPPORTED_FILE_TYPES, MAX_FILE_SIZE_MB
from corpus_manager.utils.vertex_ai import (
    initialize_vertex_ai, 
    find_corpus, 
    get_corpus_documents,
    get_corpus_stats,
    upload_document,
    delete_document
)
from corpus_manager.utils.formatters import (
    format_file_size, 
    format_date, 
    format_resource_id
)


def load_lottieurl(url: str):
    """Load Lottie animation from URL."""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


def create_file_type_chart(stats):
    """Create an interactive file type distribution chart."""
    if not stats['file_types']:
        return None
    
    fig = px.pie(
        values=list(stats['file_types'].values()),
        names=list(stats['file_types'].keys()),
        title="Document Types Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        height=300,
        showlegend=True,
        title_font_size=16,
        font=dict(size=12)
    )
    return fig


def create_corpus_metrics_chart(stats):
    """Create a gauge chart for corpus health."""
    # Simple health metric based on document count
    health_score = min(100, (stats['total_documents'] / 10) * 100)  # 10 docs = 100% health
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = health_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Corpus Health Score"},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig


def render_dashboard_page(corpus_resource_name, documents, stats):
    """Render the main dashboard page."""
    # Header with animation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        colored_header(
            label="📚 Corpus Analytics Dashboard",
            description="Real-time insights into your RAG corpus",
            color_name="blue-70"
        )
    
    with col2:
        # Load Lottie animation
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"  # Books animation
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=100, key="dashboard_animation")
    
    add_vertical_space(2)
    
    # Enhanced metrics with styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📄 Total Documents",
            value=stats['total_documents'],
            delta=f"+{stats['total_documents']}" if stats['total_documents'] > 0 else None
        )
    
    with col2:
        st.metric(
            label="💾 Total Size",
            value=format_file_size(stats['total_size']),
            delta="Optimized" if stats['total_size'] > 0 else None
        )
    
    with col3:
        file_types_count = len(stats['file_types'])
        st.metric(
            label="📋 File Types",
            value=file_types_count,
            delta=f"{file_types_count} types" if file_types_count > 0 else None
        )
    
    with col4:
        latest_upload = stats['latest_upload']
        if latest_upload:
            st.metric(
                label="⏰ Latest Upload",
                value=format_date(latest_upload),
                delta="Recent"
            )
        else:
            st.metric(label="⏰ Latest Upload", value="No uploads")
    
    # Apply metric card styling
    style_metric_cards(
        background_color="#FFFFFF",
        border_left_color="#686664",
        border_color="#000000",
        box_shadow="#F71938"
    )
    
    add_vertical_space(2)
    
    # Charts section
    if documents:
        col1, col2 = st.columns(2)
        
        with col1:
            # File type distribution
            file_chart = create_file_type_chart(stats)
            if file_chart:
                st.plotly_chart(file_chart, use_container_width=True)
        
        with col2:
            # Corpus health gauge
            health_chart = create_corpus_metrics_chart(stats)
            st.plotly_chart(health_chart, use_container_width=True)
    
    # Technical details in an expander
    with st.expander("🔧 Technical Configuration", expanded=False):
        st.code(f"""
Corpus Resource: {corpus_resource_name}
Project ID: {corpus_resource_name.split('/')[1] if '/' in corpus_resource_name else 'N/A'}
Location: {corpus_resource_name.split('/')[3] if '/' in corpus_resource_name else 'N/A'}
Total Documents: {stats['total_documents']}
        """)


def render_upload_page(corpus_resource_name):
    """Render the document upload page."""
    colored_header(
        label="📤 Upload Documents",
        description="Add new report cards and documents to your corpus",
        color_name="green-70"
    )
    
    # Animation for upload
    col1, col2 = st.columns([3, 1])
    
    with col2:
        lottie_url = "https://assets4.lottiefiles.com/packages/lf20_u4yrau.json"  # Upload animation
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=150, key="upload_animation")
    
    with col1:
        add_vertical_space(2)
        
        uploaded_file = st.file_uploader(
            "Choose a file to upload",
            type=SUPPORTED_FILE_TYPES,
            help=f"Supported formats: {', '.join(SUPPORTED_FILE_TYPES)}. Max size: {MAX_FILE_SIZE_MB}MB"
        )
        
        if uploaded_file is not None:
            # Enhanced file info display
            file_size = len(uploaded_file.getvalue())
            
            # File info card
            st.info(f"""
            📄 **File Information**
            - Name: {uploaded_file.name}
            - Size: {format_file_size(file_size)}
            - Type: {uploaded_file.type}
            """)
            
            # Progress visualization
            size_percentage = min(100, (file_size / (MAX_FILE_SIZE_MB * 1024 * 1024)) * 100)
            st.progress(size_percentage / 100)
            st.caption(f"File size: {size_percentage:.1f}% of maximum allowed")
            
            # Check file size
            if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
                st.error(f"❌ File size ({format_file_size(file_size)}) exceeds maximum allowed size ({MAX_FILE_SIZE_MB}MB)")
            else:
                add_vertical_space(1)
                
                # Enhanced upload button
                if st.button("🚀 Upload to Corpus", type="primary", use_container_width=True):
                    with st.spinner("Uploading document to corpus..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            progress_bar.progress((i + 1) / 100)
                        
                        if upload_document(uploaded_file, corpus_resource_name):
                            st.success(f"✅ Successfully uploaded '{uploaded_file.name}' to the corpus!")
                            st.balloons()  # Celebration animation
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("❌ Failed to upload document. Please try again.")


def render_documents_page(documents):
    """Render the documents management page."""
    colored_header(
        label="📄 Document Management",
        description="View and manage documents in your corpus",
        color_name="violet-70"
    )
    
    if not documents:
        # Empty state with animation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            lottie_url = "https://assets1.lottiefiles.com/packages/lf20_ysas5vsj.json"  # Empty state
            lottie_json = load_lottieurl(lottie_url)
            if lottie_json:
                st_lottie(lottie_json, height=200, key="empty_state")
            st.warning("No documents found in the corpus.")
            st.info("Upload your first document using the Upload tab.")
        return
    
    # Documents table with enhanced styling
    for i, doc in enumerate(documents):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 2, 2, 1])
            
            with col1:
                st.markdown(f"📄 **{doc['display_name']}**")
            
            with col2:
                st.markdown(f"`{format_file_size(doc['size_bytes'])}`")
            
            with col3:
                st.markdown(f"📅 {format_date(doc['create_time']) if doc['create_time'] else 'Unknown'}")
            
            with col4:
                st.markdown(f"🔗 `{format_resource_id(doc['name'])}`")
            
            with col5:
                if stateful_button("🗑️", key=f"delete_{i}", help=f"Delete {doc['display_name']}"):
                    st.session_state[f'confirm_delete_{i}'] = True
                    st.rerun()
            
            # Confirmation dialog
            if st.session_state.get(f'confirm_delete_{i}', False):
                st.warning(f"⚠️ Delete **{doc['display_name']}**? This action cannot be undone.")
                
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("✅ Confirm Delete", key=f"confirm_yes_{i}", type="primary"):
                        with st.spinner(f"Deleting {doc['display_name']}..."):
                            if delete_document(doc['name'], doc['display_name']):
                                st.success(f"✅ Successfully deleted '{doc['display_name']}'")
                                st.session_state[f'confirm_delete_{i}'] = False
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error(f"❌ Failed to delete '{doc['display_name']}'")
                
                with col_no:
                    if st.button("❌ Cancel", key=f"confirm_no_{i}"):
                        st.session_state[f'confirm_delete_{i}'] = False
                        st.rerun()
                
                break
            
            st.divider()


def main():
    """Main application function with enhanced UI."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>📚 Student Report Card RAG Corpus Manager</h1>
        <p>Modern document management with AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Validate configuration
    try:
        validate_config()
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.stop()
    
    # Initialize Vertex AI
    if not initialize_vertex_ai():
        st.error("Failed to initialize Vertex AI. Please check your configuration.")
        st.stop()
    
    # Find corpus
    corpus_resource_name = find_corpus()
    if not corpus_resource_name:
        st.error("Could not find the RAG corpus. Please check your configuration.")
        st.stop()
    
    # Get documents and stats
    documents = get_corpus_documents(corpus_resource_name)
    stats = get_corpus_stats(documents)
    
    # Enhanced navigation menu
    selected = option_menu(
        menu_title=None,
        options=["📊 Dashboard", "📤 Upload", "📄 Documents", "⚙️ Settings"],
        icons=["graph-up", "upload", "files", "gear"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#667eea"},
        }
    )
    
    add_vertical_space(2)
    
    # Render selected page
    if selected == "📊 Dashboard":
        render_dashboard_page(corpus_resource_name, documents, stats)
    
    elif selected == "📤 Upload":
        render_upload_page(corpus_resource_name)
    
    elif selected == "📄 Documents":
        render_documents_page(documents)
    
    elif selected == "⚙️ Settings":
        colored_header(
            label="⚙️ System Settings",
            description="Configuration and system information",
            color_name="red-70"
        )
        
        # System status
        st.success("✅ Corpus manager is connected and operational")
        st.info("💡 This corpus is being used by your Student Report Card RAG multi-agent system")
        
        # Quick actions
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        with col2:
            if st.button("🌐 Open Vertex AI Studio", use_container_width=True):
                st.link_button(
                    "Open in Vertex AI Studio",
                    "https://console.cloud.google.com/vertex-ai/studio",
                    use_container_width=True
                )
        
        # Configuration display
        with st.expander("📋 Configuration Details", expanded=False):
            config_data = {
                "Corpus Resource": corpus_resource_name,
                "Supported File Types": ", ".join(SUPPORTED_FILE_TYPES),
                "Max File Size": f"{MAX_FILE_SIZE_MB}MB",
                "Current Documents": stats['total_documents'],
                "Total Size": format_file_size(stats['total_size'])
            }
            
            for key, value in config_data.items():
                st.text(f"{key}: {value}")


if __name__ == "__main__":
    main() 