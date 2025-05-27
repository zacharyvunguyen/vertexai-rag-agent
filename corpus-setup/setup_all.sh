#!/bin/bash

# Student Report Card RAG System - Complete Corpus Setup
# This script sets up the entire RAG corpus infrastructure

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "\n${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_status() {
    echo -e "${GREEN}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verify prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check if we're in the right directory
    if [ ! -f "../.env" ]; then
        print_error "Not in corpus-setup directory or .env file missing"
        echo "Please run from the corpus-setup directory"
        exit 1
    fi
    
    # Check if service account is activated
    if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
        print_warning "Service account not activated"
        echo "Attempting to source service account..."
        if [ -f "../keys/service-account.env" ]; then
            source ../keys/service-account.env
            print_status "✓ Service account activated"
        else
            print_error "Service account file not found"
            echo "Please run: source ../keys/service-account.env"
            exit 1
        fi
    else
        print_status "✓ Service account already activated"
    fi
    
    # Check Python environment
    if ! python --version | grep -q "3.1"; then
        print_warning "Python 3.11+ recommended"
    else
        print_status "✓ Python version OK"
    fi
    
    # Check required packages
    if ! python -c "import vertexai, google.cloud.storage" 2>/dev/null; then
        print_error "Required packages not installed"
        echo "Please run: pip install -r ../requirements.txt"
        exit 1
    fi
    
    print_status "✓ Prerequisites check completed"
}

# Step 1: Create corpus
create_corpus() {
    print_header "Step 1: Creating RAG Corpus"
    
    cd ..  # Go back to project root for correct imports
    
    if python corpus-setup/check_corpus.py; then
        print_status "✓ Corpus setup completed successfully"
    else
        print_error "Failed to create corpus"
        exit 1
    fi
    
    cd corpus-setup
}

# Step 2: Add sample documents (optional)
add_sample_documents() {
    print_header "Step 2: Adding Sample Documents (Optional)"
    
    # Check if sample data directory exists
    if [ -d "../sample-data" ]; then
        print_status "Found sample data directory"
        
        # Count files in sample data
        file_count=$(find ../sample-data -type f \( -name "*.pdf" -o -name "*.docx" -o -name "*.txt" \) | wc -l)
        
        if [ $file_count -gt 0 ]; then
            echo "Found $file_count sample files"
            read -p "Add sample documents to corpus? (y/n): " -n 1 -r
            echo
            
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                cd ..
                if python corpus-setup/add_documents.py --source local --paths sample-data --pattern "*.pdf"; then
                    print_status "✓ Sample documents added successfully"
                else
                    print_warning "Some sample documents may have failed to upload"
                fi
                cd corpus-setup
            else
                print_status "Skipping sample document upload"
            fi
        else
            print_warning "No supported files found in sample-data directory"
        fi
    else
        print_warning "No sample-data directory found"
        echo "You can add documents later with:"
        echo "  python add_documents.py --source local --paths /path/to/your/documents/"
    fi
}

# Step 3: Test corpus
test_corpus() {
    print_header "Step 3: Testing Corpus"
    
    cd ..
    
    print_status "Running corpus information check..."
    if python corpus-setup/corpus_info.py; then
        print_status "✓ Corpus information retrieved successfully"
    else
        print_warning "Could not retrieve corpus information"
    fi
    
    # Test query if corpus has documents
    print_status "Testing with sample query..."
    if python corpus-setup/query_corpus.py --query "What is a grading standard?"; then
        print_status "✓ Query test completed"
    else
        print_warning "Query test had issues (may be normal if corpus is empty)"
    fi
    
    cd corpus-setup
}

# Step 4: Validation
validate_setup() {
    print_header "Step 4: Final Validation"
    
    cd ..
    
    # Run validation
    if python corpus-setup/corpus_info.py --list-all; then
        print_status "✓ Validation completed successfully"
    else
        print_error "Validation failed"
        exit 1
    fi
    
    cd corpus-setup
}

# Main execution
main() {
    echo "================================================================"
    echo "🎓 Student Report Card RAG System - Complete Corpus Setup"
    echo "================================================================"
    echo
    echo "This script will:"
    echo "  1. Check prerequisites"
    echo "  2. Create the RAG corpus"
    echo "  3. Optionally add sample documents"
    echo "  4. Test the corpus functionality"
    echo "  5. Validate the complete setup"
    echo
    
    read -p "Continue with setup? (y/n): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled"
        exit 0
    fi
    
    # Execute setup steps
    check_prerequisites
    create_corpus
    add_sample_documents
    test_corpus
    validate_setup
    
    # Success message
    print_header "🎉 Setup Completed Successfully!"
    
    echo
    print_status "Your Student Report Card RAG corpus is ready!"
    echo
    echo "📋 What was created:"
    echo "  ✅ RAG corpus: student-report-rag-corpus"
    echo "  ✅ Embedding model: text-embedding-005"
    echo "  ✅ Chunking configuration: 512 tokens with 100 overlap"
    echo
    echo "📋 Next steps:"
    echo "  1. Add your actual report card documents:"
    echo "     python add_documents.py --source local --paths /path/to/reports/"
    echo
    echo "  2. Test queries interactively:"
    echo "     python query_corpus.py --interactive"
    echo
    echo "  3. Check corpus status anytime:"
    echo "     python corpus_info.py"
    echo
    echo "  4. Start building your Streamlit application"
    echo
    echo "🔧 Useful commands:"
    echo "  - List all corpora: python corpus_info.py --list-all"
    echo "  - Test specific query: python query_corpus.py --query \"your question\""
    echo "  - Add GCS files: python add_documents.py --source gcs --paths gs://bucket/path/"
    echo
    echo "================================================================"
    
    return 0
}

# Run main function
main "$@" 