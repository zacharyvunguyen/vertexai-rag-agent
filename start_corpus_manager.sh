#!/bin/bash

# RAG Corpus Manager Startup Script
# This script activates the student-rag environment and starts the Streamlit app

echo "🚀 Starting RAG Corpus Manager..."
echo "📦 Activating student-rag conda environment..."

# Activate conda environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate student-rag

# Kill any existing processes on port 8503
echo "🧹 Cleaning up any existing processes on port 8503..."
lsof -ti:8503 | xargs kill -9 2>/dev/null || true

# Source service account credentials
echo "🔑 Loading service account credentials..."
source keys/service-account.env

# Wait a moment for port to be freed
sleep 2

# Start the Streamlit app
echo "▶️  Starting Streamlit app on port 8503..."
echo "🌐 Open http://localhost:8503 in your browser"
echo "⚠️  Press Ctrl+C to stop the app"
echo ""

streamlit run run_corpus_manager.py --server.port 8503 