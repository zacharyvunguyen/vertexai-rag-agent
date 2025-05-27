# Student Report Card RAG System

A modern, modular RAG (Retrieval-Augmented Generation) system for managing and querying student report card documents using Google Cloud Vertex AI and Streamlit.

## 🌟 Features

### 📚 Corpus Management
- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Smart Chunking**: Optimized document processing with configurable chunk sizes
- **Metadata Tracking**: Comprehensive document information and timestamps
- **Search & Filter**: Advanced document discovery capabilities

### 🎨 Modern Web Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Minimalist UI**: Clean, professional interface inspired by modern design principles
- **Real-time Updates**: Live data refresh and instant feedback
- **Interactive Analytics**: Visual charts and statistics

### 🔧 Advanced Operations
- **Bulk Management**: Select and manage multiple documents at once
- **Safe Deletions**: Confirmation dialogs for all destructive operations
- **Document Details**: In-depth metadata and resource information
- **Error Handling**: Comprehensive error reporting and recovery

### 📊 Analytics Dashboard
- **File Type Distribution**: Visual breakdown of document types
- **Size Analytics**: Storage usage statistics and trends
- **Upload Timeline**: Historical upload tracking and patterns
- **Performance Metrics**: Real-time system statistics

## 🏗️ Architecture

### Modular Design
```
├── corpus_manager/           # Streamlit application
│   ├── app.py               # Main application entry point
│   ├── config.py            # Configuration management
│   ├── components/          # Reusable UI components
│   ├── pages/               # Page-specific functionality
│   └── utils/               # Utility functions and helpers
├── corpus-setup/            # Corpus initialization scripts
├── gcp-setup/               # Google Cloud Platform setup
└── sample/                  # Sample documents for testing
```

### Technology Stack
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Google Cloud Vertex AI RAG API
- **Storage**: Google Cloud Storage
- **Authentication**: Service Account with IAM roles
- **Environment**: Python 3.11+ with Conda

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Google Cloud Project with billing enabled
- Conda or virtual environment manager

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/zacharyvunguyen/vertexai-rag-agent.git
cd vertexai-rag-agent

# Create and activate conda environment
conda create -n student-rag python=3.11
conda activate student-rag

# Install dependencies
pip install -r requirements.txt
```

### 2. Google Cloud Setup
```bash
# Configure your environment variables
cp .env.example .env
# Edit .env with your GCP project details

# Run the automated GCP setup
cd gcp-setup
chmod +x setup-all.sh
./setup-all.sh
```

### 3. Initialize RAG Corpus
```bash
# Set up the corpus
cd corpus-setup
chmod +x setup_all.sh
./setup_all.sh

# Add sample documents (optional)
python add_documents.py --source local --paths ../sample --pattern "*.pdf"
```

### 4. Launch the Application
```bash
# Easy startup (recommended)
./start_corpus_manager.sh

# Or manual startup
conda activate student-rag
source keys/service-account.env
streamlit run run_corpus_manager.py --server.port 8503
```

Visit `http://localhost:8503` to access the application.

## 📋 Configuration

### Environment Variables
Create a `.env` file with the following configuration:

```bash
# Google Cloud Project Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Storage Configuration
BUCKET_NAME=your-documents-bucket
KNOWLEDGE_BASE_BUCKET=your-knowledge-base-bucket

# RAG Configuration
RAG_CORPUS_NAME=your-corpus-name
EMBEDDING_MODEL=text-embedding-005
GENERATIVE_MODEL=gemini-2.5-flash-002

# Processing Configuration
CHUNK_SIZE=512
CHUNK_OVERLAP=100
MAX_FILE_SIZE_MB=50
```

### Security Configuration
- Service account authentication via JSON key file
- IAM roles: Vertex AI User, Storage Admin, AI Platform Admin
- Environment-based credential management
- Secure file upload validation

## 🎯 Usage Guide

### Document Management
1. **Upload Documents**: Use the sidebar upload component
2. **View Documents**: Browse the document list with search and filters
3. **Document Details**: Click "View Details" for comprehensive metadata
4. **Delete Documents**: Individual or bulk deletion with confirmations

### Analytics
1. **File Distribution**: View charts showing document types and sizes
2. **Timeline Analysis**: Track upload patterns over time
3. **Storage Metrics**: Monitor corpus size and growth
4. **Export Data**: Download detailed analytics reports

### Bulk Operations
1. **Multi-Select**: Choose documents using checkboxes
2. **Select All**: Quick selection for entire corpus
3. **Bulk Actions**: Perform operations on selected documents
4. **Progress Tracking**: Real-time feedback on bulk operations

## 🛠️ Development

### Project Structure
- **Components**: Reusable UI elements with consistent styling
- **Pages**: Feature-specific functionality and layouts
- **Utils**: Helper functions for data processing and API calls
- **Config**: Centralized configuration management

### Adding Features
1. **New Components**: Create in `corpus_manager/components/`
2. **New Pages**: Add to `corpus_manager/pages/`
3. **New Utilities**: Extend `corpus_manager/utils/`
4. **Styling**: Update `corpus_manager/components/styles.py`

### Code Style
- Type hints for all functions
- Comprehensive docstrings
- PEP 8 compliance
- Modular design patterns

## 📊 Performance

### Optimization Features
- **Caching**: Streamlit caching for expensive operations
- **Lazy Loading**: On-demand data fetching
- **Efficient Queries**: Optimized Vertex AI API calls
- **Resource Management**: Automatic cleanup and memory management

### Scalability
- **Horizontal Scaling**: Multiple corpus support
- **Large Documents**: Chunked processing for large files
- **Concurrent Users**: Multi-user session management
- **Cloud-Native**: Leverages GCP scalability features

## 🔒 Security

### Data Protection
- Service account authentication
- Encrypted data transmission
- Secure credential storage
- Access control via IAM

### Privacy Features
- Local credential management
- No hardcoded secrets
- Environment-based configuration
- Audit logging capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Troubleshooting
- Check the [corpus-setup README](corpus-setup/README.md) for setup issues
- Verify GCP authentication and permissions
- Ensure all environment variables are correctly set

### Common Issues
- **Import Errors**: Verify conda environment activation
- **Authentication Failures**: Check service account key file
- **Upload Failures**: Verify file type and size restrictions
- **Network Timeouts**: Check GCP region and network connectivity

### Getting Help
- Review the documentation in each module
- Check the sample configuration files
- Examine the setup scripts for reference
- Create an issue for bugs or feature requests

---

**Built with ❤️ for educational data management and analysis** 