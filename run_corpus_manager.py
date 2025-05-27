#!/usr/bin/env python3
"""
Launcher script for the RAG Corpus Manager Streamlit app.
Runs the modular Streamlit application.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path so we can import our custom modules
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the main app from our corpus_manager folder
if __name__ == "__main__":
    from corpus_manager.app import main
    main() 