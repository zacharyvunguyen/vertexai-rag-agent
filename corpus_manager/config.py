"""
Configuration module for the RAG Corpus Manager Streamlit app.
Handles environment variables and app settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Vertex AI Configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION")
RAG_CORPUS_NAME = os.environ.get("RAG_CORPUS_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-005")

# Streamlit Configuration
PAGE_TITLE = "RAG Corpus Manager"
PAGE_ICON = "📚"
LAYOUT = "wide"

# App Settings
UPLOAD_CHUNK_SIZE = 512
UPLOAD_CHUNK_OVERLAP = 100
CACHE_TTL = 60  # seconds
MAX_FILE_SIZE_MB = 50

# Supported file types
SUPPORTED_FILE_TYPES = ['pdf', 'docx', 'txt']

# UI Configuration
METRICS_COLUMNS = 4
DOCUMENTS_PER_PAGE = 10

def validate_config():
    """Validate that required configuration is present."""
    required_vars = [
        ("GOOGLE_CLOUD_PROJECT", PROJECT_ID),
        ("GOOGLE_CLOUD_LOCATION", LOCATION),
        ("RAG_CORPUS_NAME", RAG_CORPUS_NAME)
    ]
    
    missing_vars = []
    for var_name, var_value in required_vars:
        if not var_value:
            missing_vars.append(var_name)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True 