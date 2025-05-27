#!/bin/bash

# Enable Google Cloud APIs for Student Report Card RAG System
# This script enables all required APIs for the project

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
    print_status "Run: gcloud config set project $GOOGLE_CLOUD_PROJECT"
    exit 1
fi

print_status "Setting up APIs for project: $GOOGLE_CLOUD_PROJECT"

# List of required APIs
APIS=(
    "aiplatform.googleapis.com"      # Vertex AI
    "storage.googleapis.com"         # Cloud Storage
    "compute.googleapis.com"         # Compute Engine (required for Vertex AI)
    "cloudbuild.googleapis.com"      # Cloud Build (for future CI/CD)
    "run.googleapis.com"             # Cloud Run (for future deployment)
)

print_status "Enabling required Google Cloud APIs..."

for api in "${APIS[@]}"; do
    print_status "Enabling $api..."
    if gcloud services enable "$api" --quiet; then
        print_status "✓ Successfully enabled $api"
    else
        print_error "✗ Failed to enable $api"
        exit 1
    fi
done

print_status "Waiting for APIs to be fully enabled..."
sleep 10

print_status "Verifying API enablement..."
for api in "${APIS[@]}"; do
    if gcloud services list --enabled --filter="name:$api" --format="value(name)" | grep -q "$api"; then
        print_status "✓ $api is enabled"
    else
        print_warning "⚠ $api may not be fully enabled yet"
    fi
done

print_status "🎉 API setup completed successfully!"
print_status "Next step: Run ./02-create-storage.sh" 