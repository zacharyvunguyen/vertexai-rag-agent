#!/bin/bash

# Create Cloud Storage buckets for Student Report Card RAG System
# This script creates and configures the required storage buckets

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Load environment variables
if [ -f "../.env" ]; then
    source ../.env
    print_status "Loaded configuration from .env file"
else
    print_error ".env file not found. Please copy config_template.env to .env"
    exit 1
fi

# Verify we're in the correct project
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ "$CURRENT_PROJECT" != "$GOOGLE_CLOUD_PROJECT" ]; then
    print_error "Current project ($CURRENT_PROJECT) doesn't match configured project ($GOOGLE_CLOUD_PROJECT)"
    exit 1
fi

print_status "Creating Cloud Storage buckets for project: $GOOGLE_CLOUD_PROJECT"

# Function to create bucket with proper configuration
create_bucket() {
    local bucket_name=$1
    local description=$2
    
    print_status "Creating bucket: $bucket_name"
    
    # Check if bucket already exists
    if gsutil ls -b gs://"$bucket_name" 2>/dev/null; then
        print_warning "Bucket $bucket_name already exists"
        return 0
    fi
    
    # Create the bucket
    if gsutil mb -p "$GOOGLE_CLOUD_PROJECT" -c STANDARD -l "$GOOGLE_CLOUD_LOCATION" gs://"$bucket_name"; then
        print_status "✓ Created bucket: $bucket_name"
        
        # Set bucket labels for organization
        gsutil label ch -l "project:student-report-rag" gs://"$bucket_name"
        gsutil label ch -l "purpose:$description" gs://"$bucket_name"
        gsutil label ch -l "environment:$ENVIRONMENT" gs://"$bucket_name"
        
        # Enable versioning for data protection
        gsutil versioning set on gs://"$bucket_name"
        print_status "✓ Enabled versioning for $bucket_name"
        
        # Set lifecycle policy to manage costs (delete old versions after 30 days)
        cat > /tmp/lifecycle.json << EOF
{
  "rule": [
    {
      "action": {"type": "Delete"},
      "condition": {
        "numNewerVersions": 3,
        "age": 30
      }
    }
  ]
}
EOF
        gsutil lifecycle set /tmp/lifecycle.json gs://"$bucket_name"
        rm /tmp/lifecycle.json
        print_status "✓ Set lifecycle policy for $bucket_name"
        
    else
        print_error "✗ Failed to create bucket: $bucket_name"
        exit 1
    fi
}

# Create document storage bucket
print_status "Setting up document storage bucket..."
create_bucket "$BUCKET_NAME" "documents"

# Create knowledge base bucket
print_status "Setting up knowledge base bucket..."
create_bucket "$KNOWLEDGE_BASE_BUCKET" "knowledge-base"

# Set up bucket permissions for document bucket (more restrictive)
print_status "Configuring permissions for document bucket..."
# Remove public access (default deny)
gsutil iam ch -d allUsers:objectViewer gs://"$BUCKET_NAME" 2>/dev/null || true
gsutil iam ch -d allAuthenticatedUsers:objectViewer gs://"$BUCKET_NAME" 2>/dev/null || true

# Set up bucket permissions for knowledge base bucket
print_status "Configuring permissions for knowledge base bucket..."
gsutil iam ch -d allUsers:objectViewer gs://"$KNOWLEDGE_BASE_BUCKET" 2>/dev/null || true
gsutil iam ch -d allAuthenticatedUsers:objectViewer gs://"$KNOWLEDGE_BASE_BUCKET" 2>/dev/null || true

# Create folder structure in document bucket
print_status "Setting up folder structure in document bucket..."
echo "# Student Report Card Documents" | gsutil cp - gs://"$BUCKET_NAME"/README.md
echo "# Processing folder for temporary files" | gsutil cp - gs://"$BUCKET_NAME"/processing/README.md
echo "# Archive folder for processed documents" | gsutil cp - gs://"$BUCKET_NAME"/archive/README.md

# Create folder structure in knowledge base bucket
print_status "Setting up folder structure in knowledge base bucket..."
echo "# Knowledge Base Storage" | gsutil cp - gs://"$KNOWLEDGE_BASE_BUCKET"/README.md
echo "# Embeddings storage" | gsutil cp - gs://"$KNOWLEDGE_BASE_BUCKET"/embeddings/README.md
echo "# Processed documents" | gsutil cp - gs://"$KNOWLEDGE_BASE_BUCKET"/processed/README.md

print_status "Verifying bucket creation..."
for bucket in "$BUCKET_NAME" "$KNOWLEDGE_BASE_BUCKET"; do
    if gsutil ls -b gs://"$bucket" >/dev/null 2>&1; then
        print_status "✓ Verified bucket: $bucket"
        # Show bucket info
        print_status "  Location: $(gsutil ls -L -b gs://"$bucket" | grep 'Location constraint:' | cut -d: -f2 | tr -d ' ')"
        print_status "  Storage class: $(gsutil ls -L -b gs://"$bucket" | grep 'Default storage class:' | cut -d: -f2 | tr -d ' ')"
    else
        print_error "✗ Failed to verify bucket: $bucket"
    fi
done

print_status "🎉 Storage setup completed successfully!"
print_status "Created buckets:"
print_status "  - Documents: gs://$BUCKET_NAME"
print_status "  - Knowledge Base: gs://$KNOWLEDGE_BASE_BUCKET"
print_status "Next step: Run ./03-setup-iam.sh" 