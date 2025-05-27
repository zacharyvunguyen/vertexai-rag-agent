#!/usr/bin/env python3
"""
Setup script for Student Report Card RAG Agent
This script installs required dependencies and sets up the environment.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return None

def install_requirements():
    """Install required packages for the RAG agent."""
    print("\n📦 Installing RAG Agent Dependencies...")
    
    # Core dependencies needed for the RAG agent
    packages = [
        "google-cloud-aiplatform[adk,agent-engines]==1.88.0",
        "google-adk",
        "python-dotenv",
        "google-auth",
        "tqdm",
        "requests",
        "pytest",  # For evaluation
    ]
    
    for package in packages:
        run_command(f"pip install {package}", f"Installing {package}")

def check_environment():
    """Check if required environment variables are set."""
    print("\n🔍 Checking Environment Configuration...")
    
    required_vars = [
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_LOCATION", 
        "RAG_CORPUS"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            print(f"❌ {var} - Not set")
        else:
            print(f"✅ {var} - Set")
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please make sure your .env file contains:")
        print("GOOGLE_CLOUD_PROJECT=student-report-rag")
        print("GOOGLE_CLOUD_LOCATION=us-central1")
        print("RAG_CORPUS=projects/student-report-rag/locations/us-central1/ragCorpora/2305843009213693952")
        return False
    
    return True

def test_imports():
    """Test that all required modules can be imported."""
    print("\n🧪 Testing Module Imports...")
    
    modules = [
        "google.adk.agents",
        "google.adk.tools.retrieval.vertex_ai_rag_retrieval",
        "vertexai.preview.rag",
        "dotenv"
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - Failed: {e}")
            return False
    
    return True

def main():
    """Main setup function."""
    print("🚀 Student Report Card RAG Agent Setup")
    print("=" * 50)
    
    # Check if we're in a conda environment
    if "CONDA_DEFAULT_ENV" not in os.environ:
        print("⚠️  Warning: You should activate your student-rag conda environment first:")
        print("conda activate student-rag")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print(f"✅ Using conda environment: {os.environ['CONDA_DEFAULT_ENV']}")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Loaded .env file")
    except ImportError:
        print("⚠️  python-dotenv not installed, will install it first...")
        run_command("pip install python-dotenv", "Installing python-dotenv")
        from dotenv import load_dotenv
        load_dotenv()
    
    # Install requirements
    install_requirements()
    
    # Check environment
    env_ok = check_environment()
    
    # Test imports
    imports_ok = test_imports()
    
    print("\n" + "=" * 50)
    if env_ok and imports_ok:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Test the agent: python -c 'from rag.agent import root_agent; print(\"Agent loaded successfully!\")'")
        print("2. Run evaluation: python -m pytest eval/")
        print("3. Deploy agent: python deployment/deploy.py")
    else:
        print("❌ Setup completed with errors. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 