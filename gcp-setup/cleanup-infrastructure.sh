#!/bin/bash

# Cleanup Google Cloud infrastructure for Student Report Card RAG System
# This script removes all created resources - USE WITH CAUTION!

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_header() {
    echo -e "${BLUE}[CLEANUP]${NC} $1"
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

print_header "⚠️  DANGER ZONE: Infrastructure Cleanup for $GOOGLE_CLOUD_PROJECT ⚠️"
print_warning "This will permanently delete:"
print_warning "  - Cloud Storage buckets and ALL data"
print_warning "  - Service accounts and keys"
print_warning "  - IAM role bindings"
print_warning ""
print_warning "This action CANNOT be undone!"
print_warning ""

# Confirmation prompts
read -p "Are you sure you want to proceed? Type 'DELETE' to confirm: " confirm
if [ "$confirm" != "DELETE" ]; then
    print_status "Cleanup cancelled. No resources were deleted."
    exit 0
fi

read -p "Last chance! Type the project name '$GOOGLE_CLOUD_PROJECT' to proceed: " project_confirm
if [ "$project_confirm" != "$GOOGLE_CLOUD_PROJECT" ]; then
    print_status "Project name didn't match. Cleanup cancelled."
    exit 0
fi

print_header "Starting infrastructure cleanup..."

# Service account details
SERVICE_ACCOUNT_EMAIL="student-report-rag-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com"

# 1. Delete Cloud Storage buckets
print_header "1. Deleting Cloud Storage buckets"

for bucket in "$BUCKET_NAME" "$KNOWLEDGE_BASE_BUCKET"; do
    if gsutil ls -b gs://"$bucket" >/dev/null 2>&1; then
        print_status "Deleting bucket: $bucket"
        # Delete all objects first (including versions)
        gsutil -m rm -r gs://"$bucket"/** 2>/dev/null || true
        # Delete the bucket
        gsutil rb gs://"$bucket"
        print_status "✓ Deleted bucket: $bucket"
    else
        print_warning "Bucket $bucket doesn't exist or already deleted"
    fi
done

# 2. Remove IAM role bindings
print_header "2. Removing IAM role bindings"

ROLES=(
    "roles/aiplatform.user"
    "roles/storage.objectAdmin"
    "roles/logging.logWriter"
    "roles/monitoring.metricWriter"
)

for role in "${ROLES[@]}"; do
    print_status "Removing role binding: $role"
    gcloud projects remove-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
        --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
        --role="$role" \
        --quiet 2>/dev/null || true
    print_status "✓ Removed role binding: $role"
done

# 3. Delete service account keys
print_header "3. Deleting service account keys"

KEY_FILE="../keys/service-account-key.json"
if [ -f "$KEY_FILE" ]; then
    print_status "Deleting local service account key: $KEY_FILE"
    rm "$KEY_FILE"
    print_status "✓ Deleted local key file"
fi

# List and delete all keys for the service account
if gcloud iam service-accounts describe "$SERVICE_ACCOUNT_EMAIL" >/dev/null 2>&1; then
    print_status "Deleting all keys for service account..."
    for key_id in $(gcloud iam service-accounts keys list --iam-account="$SERVICE_ACCOUNT_EMAIL" --format="value(name)" | grep -v "system-managed"); do
        if [ -n "$key_id" ]; then
            gcloud iam service-accounts keys delete "$key_id" --iam-account="$SERVICE_ACCOUNT_EMAIL" --quiet
            print_status "✓ Deleted key: $key_id"
        fi
    done
fi

# 4. Delete service account
print_header "4. Deleting service account"

if gcloud iam service-accounts describe "$SERVICE_ACCOUNT_EMAIL" >/dev/null 2>&1; then
    print_status "Deleting service account: $SERVICE_ACCOUNT_EMAIL"
    gcloud iam service-accounts delete "$SERVICE_ACCOUNT_EMAIL" --quiet
    print_status "✓ Deleted service account"
else
    print_warning "Service account doesn't exist or already deleted"
fi

# 5. Clean up local files
print_header "5. Cleaning up local files"

# Remove keys directory if empty
if [ -d "../keys" ]; then
    if [ -z "$(ls -A ../keys)" ]; then
        rmdir ../keys
        print_status "✓ Removed empty keys directory"
    else
        print_warning "Keys directory not empty, keeping it"
    fi
fi

# Remove service account environment file
SERVICE_ACCOUNT_ENV="../keys/service-account.env"
if [ -f "$SERVICE_ACCOUNT_ENV" ]; then
    rm "$SERVICE_ACCOUNT_ENV"
    print_status "✓ Deleted service account environment file"
fi

# 6. Summary
print_header "Cleanup Summary"

print_status "🧹 Infrastructure cleanup completed!"
print_status ""
print_status "Deleted resources:"
print_status "  ✓ Cloud Storage buckets"
print_status "  ✓ Service account and keys"
print_status "  ✓ IAM role bindings"
print_status "  ✓ Local credential files"
print_status ""
print_warning "Note: APIs remain enabled (they don't cost anything when unused)"
print_warning "Note: The Google Cloud project itself still exists"
print_status ""
print_status "To completely remove everything:"
print_status "  1. Disable APIs if desired: gcloud services disable [api-name]"
print_status "  2. Delete the project: gcloud projects delete $GOOGLE_CLOUD_PROJECT"
print_status ""
print_status "To recreate infrastructure, run the setup scripts again." 