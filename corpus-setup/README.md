# Corpus Management Scripts

This directory contains scripts for managing Vertex AI RAG corpora for the Student Report Card system.

## Scripts Overview

### Core Management Scripts

1. **`check_corpus.py`** - Check and create the main corpus
   - Lists existing corpora
   - Creates the student report card corpus if needed
   - Configures embedding model (text-embedding-005)

2. **`add_documents.py`** - Add documents to corpus
   - Upload documents from local files or GCS paths
   - Support for PDF, DOCX, and TXT files
   - Batch processing capabilities

3. **`query_corpus.py`** - Test corpus queries
   - Interactive query testing
   - Displays retrieved context and scores
   - Useful for validating corpus content

4. **`corpus_info.py`** - Get detailed corpus information
   - Shows corpus statistics
   - Lists all documents in corpus
   - Displays embedding configuration

5. **`cleanup_corpus.py`** - Clean up corpus resources
   - Remove specific documents
   - Delete entire corpus (with confirmation)
   - Bulk cleanup operations

### Utility Scripts

- **`setup_all.sh`** - Run complete corpus setup
- **`validate_setup.sh`** - Verify corpus configuration

## Prerequisites

Before running these scripts, ensure you have:

1. **Environment Setup**:
   ```bash
   # Activate your conda environment
   conda activate student-rag
   
   # Source service account credentials
   source ../keys/service-account.env
   ```

2. **Configuration**:
   - `.env` file with proper configuration
   - Service account with appropriate permissions
   - Google Cloud project with Vertex AI enabled

## Usage

### 1. Initial Corpus Setup

```bash
# Check and create the main corpus
python check_corpus.py
```

This will:
- ✅ List any existing corpora
- ✅ Create `student-report-rag-corpus` if it doesn't exist
- ✅ Configure with text-embedding-005 model

### 2. Add Sample Documents

```bash
# Add documents from Cloud Storage
python add_documents.py --source gcs --paths gs://your-bucket/sample-reports/

# Add local files
python add_documents.py --source local --paths ./sample-data/
```

### 3. Test Queries

```bash
# Interactive query testing
python query_corpus.py

# Single query test
python query_corpus.py --query "What does 'approaching standard' mean in math?"
```

### 4. Monitor Corpus

```bash
# Get detailed corpus information
python corpus_info.py

# Specific corpus details
python corpus_info.py --corpus student-report-rag-corpus
```

### 5. Cleanup (if needed)

```bash
# Remove specific documents
python cleanup_corpus.py --remove-doc DOCUMENT_ID

# Delete entire corpus (careful!)
python cleanup_corpus.py --delete-corpus student-report-rag-corpus
```

## Complete Setup Workflow

For first-time setup, run these in order:

```bash
# 1. Navigate to corpus setup directory
cd corpus-setup

# 2. Ensure environment is ready
source ../keys/service-account.env

# 3. Create the corpus
python check_corpus.py

# 4. Add sample documents (optional)
python add_documents.py --source local --paths ../sample-data/

# 5. Test with a query
python query_corpus.py --query "Explain grading standards"

# 6. Verify setup
python corpus_info.py
```

## Configuration

The scripts use environment variables from your `.env` file:

```env
GOOGLE_CLOUD_PROJECT=student-report-rag
GOOGLE_CLOUD_LOCATION=us-central1
RAG_CORPUS_NAME=student-report-rag-corpus
BUCKET_NAME=student-report-rag-documents
```

## Troubleshooting

### Common Issues

1. **Authentication Error**:
   ```bash
   # Ensure service account is activated
   source ../keys/service-account.env
   ```

2. **Import Errors**:
   ```bash
   # Run from project root, not from corpus-setup directory
   cd .. && python corpus-setup/check_corpus.py
   ```

3. **Corpus Already Exists**:
   - Scripts will detect existing corpora and skip creation
   - Use `corpus_info.py` to inspect existing corpus

4. **Permission Denied**:
   ```bash
   # Verify service account has proper roles
   cd ../gcp-setup && ./04-verify-setup.sh
   ```

## Next Steps

After corpus setup:

1. **Development**: Start building your Streamlit application
2. **Data Upload**: Begin adding real report card documents
3. **Query Testing**: Test various natural language queries
4. **Integration**: Connect corpus to your RAG application

## Security Notes

- ⚠️ Never commit documents containing real student data
- ✅ Use sample/anonymized data for testing
- ✅ Ensure proper access controls on production corpora
- ✅ Regular cleanup of test data

---

**Status**: Corpus management scripts ready ✅ 