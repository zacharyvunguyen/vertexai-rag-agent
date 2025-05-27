#!/usr/bin/env python3
"""
Test script for Student Report Card RAG Agent
This script tests the agent with sample queries to verify it's working correctly.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_agent_import():
    """Test that the agent can be imported successfully."""
    try:
        from rag.agent import root_agent
        print("✅ Agent imported successfully")
        return root_agent
    except ImportError as e:
        print(f"❌ Failed to import agent: {e}")
        return None

def test_basic_query(agent):
    """Test the agent with a basic query."""
    print("\n🧪 Testing basic query...")
    
    try:
        # Test query about student performance
        query = "What information is available about the student's performance?"
        print(f"Query: {query}")
        
        response = agent.run_live(query)
        print(f"Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return False

def test_math_query(agent):
    """Test the agent with a mathematics-specific query."""
    print("\n🧪 Testing mathematics query...")
    
    try:
        # Test query about mathematics grades
        query = "What are the mathematics grades and scores shown in the report card?"
        print(f"Query: {query}")
        
        response = agent.run_live(query)
        print(f"Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Math query failed: {e}")
        return False

def test_casual_conversation(agent):
    """Test that the agent handles casual conversation without using retrieval."""
    print("\n🧪 Testing casual conversation...")
    
    try:
        # Test casual greeting
        query = "Hello, how are you?"
        print(f"Query: {query}")
        
        response = agent.run_live(query)
        print(f"Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Casual conversation failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Student Report Card RAG Agent Tests")
    print("=" * 50)
    
    # Check environment
    required_vars = ["GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION", "RAG_CORPUS"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please run the setup script first: python setup_rag_agent.py")
        sys.exit(1)
    
    print(f"✅ Environment configured")
    print(f"   Project: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
    print(f"   Location: {os.getenv('GOOGLE_CLOUD_LOCATION')}")
    print(f"   Corpus: {os.getenv('RAG_CORPUS')}")
    
    # Test agent import
    agent = test_agent_import()
    if not agent:
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Basic Query", lambda: test_basic_query(agent)),
        ("Mathematics Query", lambda: test_math_query(agent)),
        ("Casual Conversation", lambda: test_casual_conversation(agent)),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your RAG agent is working correctly.")
        print("\nNext steps:")
        print("1. Run evaluation: python -m pytest eval/")
        print("2. Deploy agent: python deployment/deploy.py")
        print("3. Test deployed agent: python deployment/run.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 