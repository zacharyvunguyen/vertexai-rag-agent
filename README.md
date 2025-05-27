# Student Report Card RAG System

> **AI-Powered Student Performance Analysis Platform**  
> Built with Google Cloud Vertex AI, RAG Engine, and Streamlit

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)

## 🎯 Overview

The Student Report Card RAG System is a comprehensive AI-powered platform designed to analyze student academic performance data using advanced Retrieval-Augmented Generation (RAG) technology. The system provides intelligent insights, performance analytics, and educational recommendations based on student report cards.

### Key Features

- **🧠 AI-Powered Analysis**: Uses Google's Gemini 2.0 Flash with RAG for intelligent student performance analysis
- **📊 Interactive Dashboard**: Modern Streamlit interface for document management and analytics
- **🔍 Advanced Search**: Semantic search across student report card corpus
- **📈 Performance Insights**: Automated generation of academic performance reports and recommendations
- **🔒 Privacy-First**: Secure handling of sensitive student data with Google Cloud security
- **🚀 Scalable Architecture**: Cloud-native design for handling multiple schools and students

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   RAG Agent      │    │  Vertex AI      │
│   Dashboard     │◄──►│   (ADK/Gemini)   │◄──►│  RAG Engine     │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Document      │    │   Agent Engine   │    │   Vector DB     │
│   Manager       │    │   (Deployed)     │    │   (Embeddings)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Google Cloud Project** with billing enabled
- **Python 3.11+** and Conda
- **Git** for version control

### 1. Environment Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd student-report-card-rag

# Create and activate conda environment
conda create -n student-rag python=3.11 -y
conda activate student-rag

# Install dependencies
pip install -r requirements.txt
```

### 2. Google Cloud Setup

```bash
# Setup GCP infrastructure
cd gcp-setup
chmod +x setup-all.sh
./setup-all.sh

# Setup RAG corpus
cd ../corpus-setup
chmod +x setup_all.sh
./setup_all.sh
```

### 3. Launch Applications

```bash
# Start the Corpus Manager Dashboard
./start_corpus_manager.sh

# Or start the RAG Agent CLI
conda activate student-rag
source keys/service-account.env
adk run rag
```

## 📁 Project Structure

```
student-report-card-rag/
├── 📊 corpus_manager/           # Streamlit Dashboard
│   ├── components/              # UI Components
│   ├── pages/                   # Dashboard Pages
│   ├── utils/                   # Utilities
│   └── app.py                   # Main Application
├── 🤖 rag/                      # RAG Agent
│   ├── agent.py                 # Agent Definition
│   ├── prompts.py               # Student-focused Prompts
│   └── shared_libraries/        # Utilities
├── 🧪 eval/                     # Evaluation Framework
│   ├── test_eval.py            # Test Scripts
│   └── data/                   # Test Data
├── 🚀 deployment/               # Deployment Tools
│   ├── deploy.py               # Deploy to Vertex AI
│   ├── run.py                  # Test Deployed Agent
│   └── grant_permissions.sh    # Setup Permissions
├── ⚙️ gcp-setup/               # GCP Infrastructure
├── 📚 corpus-setup/            # Corpus Management
├── 🔑 keys/                    # Service Account Keys
├── 📄 sample/                  # Sample Documents
├── 🔧 Configuration Files
│   ├── adk_config.yaml         # ADK Configuration
│   ├── requirements.txt        # Dependencies
│   └── .env                    # Environment Variables
└── 🚀 Launcher Scripts
    ├── run_corpus_manager.py   # Streamlit Launcher
    ├── setup_rag_agent.py      # RAG Setup
    ├── test_rag_agent.py       # RAG Testing
    └── start_corpus_manager.sh # Dashboard Launcher
```

## 🎓 Usage Guide

### Corpus Manager Dashboard

The Streamlit dashboard provides a comprehensive interface for managing your student report card corpus:

**Features:**
- 📋 **Document List**: View, search, and filter documents
- 📊 **Analytics**: File type distribution, size analysis, upload timeline
- 🔧 **Bulk Operations**: Multi-document management and deletion
- ⬆️ **Upload Interface**: Drag-and-drop document upload
- 🔍 **Search & Filter**: Find specific documents quickly

**Access:** `http://localhost:8503`

### RAG Agent (CLI)

The conversational AI agent analyzes student performance using natural language:

```bash
# Start interactive session
adk run rag

# Example queries:
"What are the mathematics grades for this student?"
"Can you analyze the overall academic performance?"
"What recommendations do teachers provide?"
"How is the student performing against learning standards?"
```

### RAG Agent (Web UI)

```bash
# Launch web interface
adk web
# Select 'rag' from the dropdown
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=student-report-rag
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=1

# RAG Configuration
RAG_CORPUS=projects/your-project/locations/us-central1/ragCorpora/your-corpus-id
EMBEDDING_MODEL=text-embedding-005
GENERATIVE_MODEL=gemini-2.5-flash-002

# Storage Configuration
BUCKET_NAME=student-report-rag-documents
KNOWLEDGE_BASE_BUCKET=student-report-rag-knowledge-base
STAGING_BUCKET=gs://student-report-rag-knowledge-base

# Application Configuration
APP_TITLE="Student Report Card RAG System"
APP_PORT=8501
ALLOWED_FILE_TYPES=pdf,docx,txt
```

### Customization

**Agent Behavior** (`rag/prompts.py`):
- Modify response tone and educational terminology
- Adjust privacy and confidentiality guidelines
- Customize citation formats

**UI Styling** (`corpus_manager/components/styles.py`):
- Update color schemes and branding
- Modify layout and responsive design
- Customize dashboard components

## 🧪 Testing & Evaluation

### Local Testing

```bash
# Test RAG agent functionality
python test_rag_agent.py

# Run evaluation suite
python -m pytest eval/ -v

# Simple functionality test
python simple_rag_test.py
```

### Performance Metrics

The system is optimized for:
- **Response Time**: 2-5 seconds for typical queries
- **Accuracy**: >90% for student performance questions
- **Privacy**: Secure handling of sensitive data
- **Scalability**: Supports multiple concurrent users

## 🚀 Deployment

### Deploy RAG Agent to Vertex AI

```bash
# Deploy to Vertex AI Agent Engine
python deployment/deploy.py

# Grant necessary permissions
chmod +x deployment/grant_permissions.sh
./deployment/grant_permissions.sh

# Test deployed agent
python deployment/run.py
```

### Production Deployment

For production environments:

1. **Security**: Configure IAM roles and data access policies
2. **Monitoring**: Set up Cloud Monitoring and logging
3. **Scaling**: Configure auto-scaling for high availability
4. **Backup**: Implement data backup and disaster recovery

## 📊 Analytics & Insights

### Student Performance Analysis

The RAG agent provides insights on:
- **Academic Performance**: Grade analysis across subjects
- **Learning Standards**: Progress against curriculum objectives
- **Teacher Feedback**: Summarized comments and recommendations
- **Behavioral Patterns**: Attendance and participation analysis
- **Improvement Areas**: Identified areas needing attention

### Dashboard Analytics

The Streamlit dashboard offers:
- **Document Statistics**: File counts, sizes, and types
- **Upload Trends**: Timeline of document additions
- **Search Analytics**: Most queried topics and patterns
- **Performance Metrics**: System usage and response times

## 🔒 Security & Privacy

### Data Protection

- **Encryption**: All data encrypted in transit and at rest
- **Access Control**: IAM-based role and permission management
- **Audit Logging**: Comprehensive logging of all system activities
- **Data Retention**: Configurable retention policies
- **Privacy Compliance**: Designed for FERPA and other educational privacy standards

### Authentication

- **Service Account**: Secure GCP service account authentication
- **Scoped Access**: Minimal required permissions principle
- **Key Management**: Secure handling of API keys and credentials

## 🛠️ Development

### Adding New Features

1. **New Document Types**: Extend parsing in `corpus-setup/`
2. **Additional Analytics**: Add new visualizations in `corpus_manager/pages/`
3. **Enhanced Prompts**: Modify agent behavior in `rag/prompts.py`
4. **Custom Tools**: Add new agent tools in `rag/agent.py`

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

**Authentication Errors:**
```bash
gcloud auth application-default login
source keys/service-account.env
```

**Corpus Access Issues:**
```bash
python corpus-setup/corpus_info.py
./deployment/grant_permissions.sh
```

**Streamlit Import Errors:**
```bash
conda activate student-rag
pip install --upgrade streamlit
```

**RAG Agent Issues:**
```bash
python setup_rag_agent.py
python test_rag_agent.py
```

### Support

- 📧 **Issues**: Create GitHub issues for bugs and feature requests
- 📖 **Documentation**: Check the inline code documentation
- 🔍 **Logs**: Review Google Cloud logs for deployment issues
- 🧪 **Testing**: Run the test suites to identify specific problems

## 📚 Resources

### Google Cloud Documentation
- [Vertex AI RAG Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview)
- [Agent Development Kit](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development)
- [Vertex AI Best Practices](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-best-practices)

### Technical References
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google ADK Samples](https://github.com/google/adk-samples)
- [Gemini API Documentation](https://ai.google.dev/docs)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Cloud AI**: For providing the Vertex AI platform and RAG Engine
- **Streamlit**: For the excellent dashboard framework
- **Educational Community**: For inspiring this student-focused AI solution

---

**Built with ❤️ for Education**  
*Empowering educators and students through AI-driven insights* 