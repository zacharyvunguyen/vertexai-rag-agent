"""
Analytics page for the RAG Corpus Manager.
Displays charts and visualizations of corpus data including file type distribution,
size distribution, and upload timeline.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict
from ..utils.formatters import format_document_name


def render_analytics(documents: List[Dict]):
    """Render the analytics page with charts and visualizations."""
    if not documents:
        st.info("No data available for analytics. Upload some documents first!")
        return
    
    # File type distribution
    st.markdown("### 📊 File Type Distribution")
    _render_file_type_chart(documents)
    
    st.markdown("---")
    
    # Size distribution
    st.markdown("### 📈 Document Sizes")
    _render_size_chart(documents)
    
    st.markdown("---")
    
    # Upload timeline
    st.markdown("### 📅 Upload Timeline")
    _render_timeline_chart(documents)


def _render_file_type_chart(documents: List[Dict]):
    """Render file type distribution chart."""
    file_type_data = {}
    for doc in documents:
        ext = doc['display_name'].lower().split('.')[-1] if '.' in doc['display_name'] else 'unknown'
        file_type_data[ext] = file_type_data.get(ext, 0) + 1
    
    if file_type_data:
        df_types = pd.DataFrame(list(file_type_data.items()), columns=['File Type', 'Count'])
        st.bar_chart(df_types.set_index('File Type'))
        
        # Show breakdown table
        with st.expander("📋 View detailed breakdown"):
            # Calculate percentages
            total = sum(file_type_data.values())
            breakdown_data = []
            for file_type, count in file_type_data.items():
                percentage = (count / total * 100) if total > 0 else 0
                breakdown_data.append({
                    'File Type': file_type.upper(),
                    'Count': count,
                    'Percentage': f"{percentage:.1f}%"
                })
            
            df_breakdown = pd.DataFrame(breakdown_data)
            st.dataframe(df_breakdown, use_container_width=True)
    else:
        st.info("No file type data available")


def _render_size_chart(documents: List[Dict]):
    """Render document size distribution chart."""
    size_data = []
    for doc in documents:
        size_data.append({
            'Document': format_document_name(doc['display_name'], max_length=25),
            'Size (MB)': doc['size_bytes'] / (1024 * 1024) if doc['size_bytes'] > 0 else 0
        })
    
    if size_data:
        df_sizes = pd.DataFrame(size_data)
        st.bar_chart(df_sizes.set_index('Document'))
        
        # Size statistics
        total_size_mb = sum(item['Size (MB)'] for item in size_data)
        avg_size_mb = total_size_mb / len(size_data) if size_data else 0
        max_size_mb = max(item['Size (MB)'] for item in size_data) if size_data else 0
        min_size_mb = min(item['Size (MB)'] for item in size_data) if size_data else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Size", f"{total_size_mb:.1f} MB")
        with col2:
            st.metric("Average Size", f"{avg_size_mb:.1f} MB")
        with col3:
            st.metric("Largest File", f"{max_size_mb:.1f} MB")
        with col4:
            st.metric("Smallest File", f"{min_size_mb:.1f} MB")
    else:
        st.info("No size data available")


def _render_timeline_chart(documents: List[Dict]):
    """Render upload timeline chart."""
    timeline_data = []
    for doc in documents:
        if doc['create_time']:
            try:
                # Handle different date formats
                if hasattr(doc['create_time'], 'date'):
                    date = doc['create_time'].date()
                else:
                    # Assume it's already a date or can be converted
                    date = doc['create_time']
                timeline_data.append({'Date': date, 'Documents': 1})
            except (AttributeError, ValueError):
                # Skip documents with invalid dates
                continue
    
    if timeline_data:
        df_timeline = pd.DataFrame(timeline_data)
        # Group by date and sum documents
        df_timeline = df_timeline.groupby('Date').sum().reset_index()
        df_timeline = df_timeline.sort_values('Date')
        
        st.line_chart(df_timeline.set_index('Date'))
        
        # Timeline statistics
        if len(df_timeline) > 1:
            first_upload = df_timeline['Date'].min()
            last_upload = df_timeline['Date'].max()
            days_span = (last_upload - first_upload).days if hasattr(last_upload - first_upload, 'days') else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("First Upload", str(first_upload))
            with col2:
                st.metric("Latest Upload", str(last_upload))
            with col3:
                st.metric("Days Span", f"{days_span}")
        
        # Show upload frequency
        with st.expander("📈 Upload frequency details"):
            st.dataframe(df_timeline, use_container_width=True)
    else:
        st.info("No timeline data available") 