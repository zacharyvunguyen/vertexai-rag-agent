"""
CSS styles for the RAG Corpus Manager Streamlit app.
Contains all custom styling for a modern, minimalist design.
"""

import streamlit as st


def apply_custom_css():
    """Apply custom CSS styles to the Streamlit app."""
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
        
        /* Custom spacing classes */
        .mt-1 { margin-top: 0.25rem; }
        .mt-2 { margin-top: 0.5rem; }
        .mt-3 { margin-top: 0.75rem; }
        .mt-4 { margin-top: 1rem; }
        
        .mb-1 { margin-bottom: 0.25rem; }
        .mb-2 { margin-bottom: 0.5rem; }
        .mb-3 { margin-bottom: 0.75rem; }
        .mb-4 { margin-bottom: 1rem; }
        
        .p-1 { padding: 0.25rem; }
        .p-2 { padding: 0.5rem; }
        .p-3 { padding: 0.75rem; }
        .p-4 { padding: 1rem; }
        
        /* Text utilities */
        .text-center { text-align: center; }
        .text-left { text-align: left; }
        .text-right { text-align: right; }
        
        .font-bold { font-weight: 700; }
        .font-semibold { font-weight: 600; }
        .font-medium { font-weight: 500; }
        
        .text-sm { font-size: 0.875rem; }
        .text-lg { font-size: 1.125rem; }
        .text-xl { font-size: 1.25rem; }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            
            .main-header {
                padding: 1.5rem;
            }
            
            .main-header h1 {
                font-size: 2rem;
            }
            
            .metric-card {
                padding: 1rem;
            }
            
            .document-item {
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True) 