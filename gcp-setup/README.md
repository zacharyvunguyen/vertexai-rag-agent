# Google Cloud Infrastructure Setup

This folder contains all the scripts and documentation needed to set up the Google Cloud infrastructure for the Student Report Card RAG system.

## Setup Order

Run the scripts in this order:

1. `01-enable-apis.sh` - Enable required Google Cloud APIs
2. `02-create-storage.sh` - Create Cloud Storage buckets
3. `03-setup-iam.sh` - Configure IAM roles and permissions
4. `04-verify-setup.sh` - Verify all resources are created correctly

## Prerequisites

- Google Cloud SDK installed and configured
- Active Google Cloud project: `student-report-rag`
- Proper authentication (Application Default Credentials)
- Required permissions to create resources

## Configuration

All configuration is read from the `.env` file in the project root. Make sure to copy `config_template.env` to `.env` and adjust any values as needed.

## Scripts Description

### 01-enable-apis.sh
Enables the required Google Cloud APIs:
- Vertex AI API (aiplatform.googleapis.com)
- Cloud Storage API (storage.googleapis.com)
- Compute Engine API (compute.googleapis.com)

### 02-create-storage.sh
Creates the Cloud Storage buckets:
- Document storage bucket
- Knowledge base bucket
- Sets up proper bucket configurations and permissions

### 03-setup-iam.sh
Configures IAM roles and service accounts:
- Creates service account for the application
- Sets up proper permissions for Vertex AI and Storage

### 04-verify-setup.sh
Verifies that all resources are created and accessible:
- Checks API enablement
- Verifies bucket creation
- Tests permissions

## Cleanup

If you need to tear down the infrastructure, use:
- `cleanup-infrastructure.sh` - Removes all created resources

## Troubleshooting

Common issues and solutions are documented in `TROUBLESHOOTING.md`. 