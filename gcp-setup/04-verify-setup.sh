#!/bin/bash

# Verify Google Cloud infrastructure setup for Student Report Card RAG System
# This script checks that all resources are created and properly configured

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
    echo -e "${BLUE}[VERIFY]${NC} $1"
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

print_header "Verifying Google Cloud infrastructure for: $GOOGLE_CLOUD_PROJECT"

# Track verification results
VERIFICATION_ERRORS=0

# Function to check and report status
check_status() {
    local description="$1"
    local command="$2"
    
    echo -n "  Checking $description... "
    
    if eval "$command" >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        ((VERIFICATION_ERRORS++))
        return 1
    fi
}

# 1. Verify APIs are enabled
print_header "1. Checking API enablement"

REQUIRED_APIS=(
    "aiplatform.googleapis.com"
    "storage.googleapis.com"
    "compute.googleapis.com"
)

for api in "${REQUIRED_APIS[@]}"; do
    check_status "$api" "gcloud services list --enabled --filter='name:$api' --format='value(name)' | grep -q '$api'"
done

# 2. Verify Cloud Storage buckets
print_header "2. Checking Cloud Storage buckets"

check_status "Document bucket ($BUCKET_NAME)" "gsutil ls -b gs://$BUCKET_NAME"
check_status "Knowledge base bucket ($KNOWLEDGE_BASE_BUCKET)" "gsutil ls -b gs://$KNOWLEDGE_BASE_BUCKET"

# Check bucket configurations
if gsutil ls -b gs://"$BUCKET_NAME" >/dev/null 2>&1; then
    print_status "Document bucket details:"
    gsutil ls -L -b gs://"$BUCKET_NAME" | grep -E "(Location|Storage class|Versioning)" | sed 's/^/    /'
fi

if gsutil ls -b gs://"$KNOWLEDGE_BASE_BUCKET" >/dev/null 2>&1; then
    print_status "Knowledge base bucket details:"
    gsutil ls -L -b gs://"$KNOWLEDGE_BASE_BUCKET" | grep -E "(Location|Storage class|Versioning)" | sed 's/^/    /'
fi

# 3. Verify Service Account
print_header "3. Checking Service Account"

SERVICE_ACCOUNT_EMAIL="student-report-rag-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com"
check_status "Service account exists" "gcloud iam service-accounts describe $SERVICE_ACCOUNT_EMAIL"

# Check service account key
KEY_FILE="../keys/service-account-key.json"
check_status "Service account key exists" "test -f $KEY_FILE"

if [ -f "$KEY_FILE" ]; then
    print_status "Service account key file size: $(ls -lh "$KEY_FILE" | awk '{print $5}')"
fi

# 4. Verify IAM permissions
print_header "4. Checking IAM permissions"

REQUIRED_ROLES=(
    "roles/aiplatform.user"
    "roles/storage.objectAdmin"
    "roles/logging.logWriter"
    "roles/monitoring.metricWriter"
)

for role in "${REQUIRED_ROLES[@]}"; do
    check_status "Role $role assigned" "gcloud projects get-iam-policy $GOOGLE_CLOUD_PROJECT --flatten='bindings[].members' --filter='bindings.role:$role AND bindings.members:serviceAccount:$SERVICE_ACCOUNT_EMAIL' --format='value(bindings.role)' | grep -q '$role'"
done

# 5. Test Vertex AI access
print_header "5. Testing Vertex AI access"

# Test if we can list Vertex AI models (basic connectivity test)
check_status "Vertex AI API access" "gcloud ai models list --region=$GOOGLE_CLOUD_LOCATION --limit=1"

# 6. Test Storage access with service account
print_header "6. Testing Storage access"

if [ -f "$KEY_FILE" ]; then
    # Temporarily set service account credentials
    export GOOGLE_APPLICATION_CREDENTIALS="$KEY_FILE"
    
    check_status "Service account storage access" "gsutil ls gs://$BUCKET_NAME"
    check_status "Service account KB storage access" "gsutil ls gs://$KNOWLEDGE_BASE_BUCKET"
    
    # Test write access
    echo "Verification test $(date)" > /tmp/verify-test.txt
    if gsutil cp /tmp/verify-test.txt gs://"$BUCKET_NAME"/test/ >/dev/null 2>&1; then
        echo -e "  Write access to document bucket... ${GREEN}✓${NC}"
        gsutil rm gs://"$BUCKET_NAME"/test/verify-test.txt >/dev/null 2>&1
    else
        echo -e "  Write access to document bucket... ${RED}✗${NC}"
        ((VERIFICATION_ERRORS++))
    fi
    rm -f /tmp/verify-test.txt
    
    unset GOOGLE_APPLICATION_CREDENTIALS
fi

# 7. Verify project quotas and limits
print_header "7. Checking project quotas"

# Check if we have sufficient quotas for Vertex AI
if gcloud compute project-info describe --format="value(quotas[].metric,quotas[].limit)" | grep -q "VERTEX_AI"; then
    print_status "Vertex AI quotas are configured"
else
    print_warning "Vertex AI quotas not found - may need to be requested"
fi

# Summary
print_header "Verification Summary"

if [ $VERIFICATION_ERRORS -eq 0 ]; then
    print_status "🎉 All checks passed! Infrastructure is ready."
    print_status ""
    print_status "Your Google Cloud infrastructure is properly configured:"
    print_status "  ✓ APIs enabled"
    print_status "  ✓ Storage buckets created"
    print_status "  ✓ Service account configured"
    print_status "  ✓ IAM permissions assigned"
    print_status "  ✓ Vertex AI accessible"
    print_status ""
    print_status "Next steps:"
    print_status "  1. Copy config_template.env to .env (if not done)"
    print_status "  2. Source service account: source keys/service-account.env"
    print_status "  3. Start developing your RAG application!"
    print_status ""
    print_status "Useful commands:"
    print_status "  - View buckets: gsutil ls"
    print_status "  - Check service account: gcloud iam service-accounts list"
    print_status "  - Monitor usage: gcloud logging read"
else
    print_error "❌ $VERIFICATION_ERRORS verification(s) failed!"
    print_error ""
    print_error "Please check the failed items above and:"
    print_error "  1. Re-run the appropriate setup script"
    print_error "  2. Check your permissions"
    print_error "  3. Verify your project configuration"
    exit 1
fi 