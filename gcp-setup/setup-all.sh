#!/bin/bash

# Master setup script for Student Report Card RAG System
# This script runs all infrastructure setup scripts in the correct order

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[SETUP]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[MASTER SETUP]${NC} $1"
}

print_header "🚀 Starting complete Google Cloud infrastructure setup"
print_header "Student Report Card RAG System"
print_status ""

# Check prerequisites
print_status "Checking prerequisites..."

# Check if .env file exists
if [ ! -f "../.env" ]; then
    print_error ".env file not found!"
    print_status "Please run: cp config_template.env .env"
    exit 1
fi

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    print_error "gcloud CLI not found!"
    print_status "Please install Google Cloud SDK first"
    exit 1
fi

# Check if gsutil is installed
if ! command -v gsutil &> /dev/null; then
    print_error "gsutil not found!"
    print_status "Please install Google Cloud SDK first"
    exit 1
fi

print_status "✓ Prerequisites check passed"
print_status ""

# Load environment to show project info
source ../.env
print_status "Setting up infrastructure for project: $GOOGLE_CLOUD_PROJECT"
print_status "Location: $GOOGLE_CLOUD_LOCATION"
print_status ""

# Confirm before proceeding
read -p "Do you want to proceed with the complete setup? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status "Setup cancelled by user"
    exit 0
fi

# Setup scripts in order
SCRIPTS=(
    "01-enable-apis.sh"
    "02-create-storage.sh" 
    "03-setup-iam.sh"
    "04-verify-setup.sh"
)

for script in "${SCRIPTS[@]}"; do
    print_header "Running $script"
    
    if [ -f "$script" ] && [ -x "$script" ]; then
        if ./"$script"; then
            print_status "✓ $script completed successfully"
        else
            print_error "✗ $script failed!"
            print_error "Setup stopped. Please check the error above and fix it."
            print_error "You can re-run this script or run individual scripts manually."
            exit 1
        fi
    else
        print_error "Script $script not found or not executable"
        exit 1
    fi
    
    print_status ""
    sleep 2  # Brief pause between scripts
done

print_header "🎉 Complete infrastructure setup finished!"
print_status ""
print_status "Your Student Report Card RAG system infrastructure is ready!"
print_status ""
print_status "Next steps:"
print_status "1. Source the service account environment:"
print_status "   source keys/service-account.env"
print_status ""
print_status "2. Start developing your RAG application"
print_status ""
print_status "3. Useful commands:"
print_status "   - View your buckets: gsutil ls"
print_status "   - Check service accounts: gcloud iam service-accounts list"
print_status "   - View project info: gcloud config list"
print_status ""
print_status "Infrastructure overview:"
print_status "  📦 Document Storage: gs://$BUCKET_NAME"
print_status "  🧠 Knowledge Base: gs://$KNOWLEDGE_BASE_BUCKET"
print_status "  🔑 Service Account: student-report-rag-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com"
print_status "  🌍 Region: $GOOGLE_CLOUD_LOCATION" 