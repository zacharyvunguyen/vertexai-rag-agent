#!/bin/bash

# Setup IAM roles and service accounts for Student Report Card RAG System
# This script creates service accounts and assigns appropriate permissions

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

print_status "Setting up IAM for project: $GOOGLE_CLOUD_PROJECT"

# Service account details
SERVICE_ACCOUNT_NAME="student-report-rag-sa"
SERVICE_ACCOUNT_EMAIL="$SERVICE_ACCOUNT_NAME@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com"
SERVICE_ACCOUNT_DISPLAY_NAME="Student Report Card RAG Service Account"

# Create service account
print_status "Creating service account: $SERVICE_ACCOUNT_NAME"
if gcloud iam service-accounts describe "$SERVICE_ACCOUNT_EMAIL" >/dev/null 2>&1; then
    print_warning "Service account $SERVICE_ACCOUNT_EMAIL already exists"
else
    if gcloud iam service-accounts create "$SERVICE_ACCOUNT_NAME" \
        --display-name="$SERVICE_ACCOUNT_DISPLAY_NAME" \
        --description="Service account for Student Report Card RAG system operations"; then
        print_status "✓ Created service account: $SERVICE_ACCOUNT_EMAIL"
    else
        print_error "✗ Failed to create service account"
        exit 1
    fi
fi

# Required IAM roles for the service account
print_status "Assigning IAM roles to service account..."

ROLES=(
    "roles/aiplatform.user"              # Vertex AI access
    "roles/storage.objectAdmin"          # Full access to storage objects
    "roles/logging.logWriter"            # Write application logs
    "roles/monitoring.metricWriter"      # Write monitoring metrics
)

for role in "${ROLES[@]}"; do
    print_status "Assigning role: $role"
    if gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
        --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
        --role="$role" \
        --quiet; then
        print_status "✓ Assigned $role"
    else
        print_warning "⚠ Failed to assign $role (may already exist)"
    fi
done

# Create and download service account key
print_status "Creating service account key..."
KEY_FILE="../keys/service-account-key.json"
mkdir -p ../keys

if [ -f "$KEY_FILE" ]; then
    print_warning "Service account key already exists at $KEY_FILE"
    read -p "Do you want to create a new key? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Keeping existing key"
    else
        rm "$KEY_FILE"
        create_new_key=true
    fi
else
    create_new_key=true
fi

if [ "$create_new_key" = true ]; then
    if gcloud iam service-accounts keys create "$KEY_FILE" \
        --iam-account="$SERVICE_ACCOUNT_EMAIL"; then
        print_status "✓ Created service account key: $KEY_FILE"
        print_warning "⚠ Keep this key secure and never commit it to version control!"
    else
        print_error "✗ Failed to create service account key"
        exit 1
    fi
fi

# Set up bucket-specific permissions
print_status "Setting up bucket-specific permissions..."

# Document bucket - service account needs full access
gsutil iam ch serviceAccount:"$SERVICE_ACCOUNT_EMAIL":objectAdmin gs://"$BUCKET_NAME"
print_status "✓ Granted objectAdmin access to document bucket"

# Knowledge base bucket - service account needs full access
gsutil iam ch serviceAccount:"$SERVICE_ACCOUNT_EMAIL":objectAdmin gs://"$KNOWLEDGE_BASE_BUCKET"
print_status "✓ Granted objectAdmin access to knowledge base bucket"

# Verify service account setup
print_status "Verifying service account setup..."

if gcloud iam service-accounts describe "$SERVICE_ACCOUNT_EMAIL" >/dev/null 2>&1; then
    print_status "✓ Service account exists and is accessible"
    
    # Show assigned roles
    print_status "Assigned roles:"
    gcloud projects get-iam-policy "$GOOGLE_CLOUD_PROJECT" \
        --flatten="bindings[].members" \
        --format="table(bindings.role)" \
        --filter="bindings.members:serviceAccount:$SERVICE_ACCOUNT_EMAIL"
else
    print_error "✗ Service account verification failed"
    exit 1
fi

# Create environment variables for the service account
print_status "Creating service account environment variables..."

cat >> ../keys/service-account.env << EOF
# Service Account Configuration
# Add these to your .env file or export them in your environment

export GOOGLE_APPLICATION_CREDENTIALS="\$(pwd)/keys/service-account-key.json"
export SERVICE_ACCOUNT_EMAIL="$SERVICE_ACCOUNT_EMAIL"

# To use these variables, run:
# source keys/service-account.env
EOF

print_status "✓ Created service account environment file: ../keys/service-account.env"

print_status "🎉 IAM setup completed successfully!"
print_status "Service account: $SERVICE_ACCOUNT_EMAIL"
print_status "Key file: $KEY_FILE"
print_status "Environment file: ../keys/service-account.env"
print_status ""
print_status "Next steps:"
print_status "1. Add keys/ to your .gitignore (if not already)"
print_status "2. Source the environment: source keys/service-account.env"
print_status "3. Run ./04-verify-setup.sh" 