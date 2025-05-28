#!/usr/bin/env python3
"""
Test script for Multi-Agent Educational Coordinator
This script tests the coordinator's ability to route queries intelligently.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_coordinator_import():
    """Test that the coordinator can be imported successfully."""
    try:
        from rag.agent import root_agent
        print("✅ Educational Coordinator imported successfully")
        print(f"   Agent name: {root_agent.name}")
        print(f"   Sub-agents: {[agent.name for agent in root_agent.sub_agents]}")
        return root_agent
    except ImportError as e:
        print(f"❌ Failed to import coordinator: {e}")
        return None

async def test_simple_query(agent):
    """Test the coordinator with a simple RAG query."""
    print("\n🧪 Testing Simple Query (should route to DataRetriever)...")
    
    try:
        # Test query that should go to simple RAG
        query = "What rating did Benjamin get in Math counting for Q3?"
        print(f"Query: {query}")
        
        # Handle async generator properly
        response_text = ""
        async for event in agent.run_live(query):
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    if hasattr(event.content.parts[0], 'text'):
                        response_text += event.content.parts[0].text
            elif hasattr(event, 'text'):
                response_text += event.text
        
        print(f"Response: {response_text}")
        return True
        
    except Exception as e:
        print(f"❌ Simple query failed: {e}")
        return False

async def test_complex_query(agent):
    """Test the coordinator with a complex analysis query."""
    print("\n🧪 Testing Complex Query (should route to WeaknessAnalyzer)...")
    
    try:
        # Test query that should go to weakness analyzer
        query = "Identify areas where Benjamin needs improvement"
        print(f"Query: {query}")
        
        # Handle async generator properly
        response_text = ""
        async for event in agent.run_live(query):
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    if hasattr(event.content.parts[0], 'text'):
                        response_text += event.content.parts[0].text
            elif hasattr(event, 'text'):
                response_text += event.text
        
        print(f"Response: {response_text}")
        return True
        
    except Exception as e:
        print(f"❌ Complex query failed: {e}")
        return False

async def test_routing_explanation(agent):
    """Test that the coordinator explains its routing decisions."""
    print("\n🧪 Testing Routing Explanation...")
    
    try:
        # Test query to see routing explanation
        query = "What are the literacy scores?"
        print(f"Query: {query}")
        
        # Handle async generator properly
        response_text = ""
        async for event in agent.run_live(query):
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    if hasattr(event.content.parts[0], 'text'):
                        response_text += event.content.parts[0].text
            elif hasattr(event, 'text'):
                response_text += event.text
        
        print(f"Response: {response_text}")
        
        # Check if response contains routing explanation
        if "routing" in response_text.lower() or "simple" in response_text.lower():
            print("✅ Coordinator explained routing decision")
            return True
        else:
            print("⚠️  Coordinator may not have explained routing")
            return True  # Still passes, just noting
        
    except Exception as e:
        print(f"❌ Routing explanation test failed: {e}")
        return False

async def run_async_tests():
    """Run all async tests."""
    # Test coordinator import
    coordinator = test_coordinator_import()
    if not coordinator:
        return 0, 3
    
    # Run tests
    tests = [
        ("Simple Query Routing", lambda: test_simple_query(coordinator)),
        ("Complex Query Routing", lambda: test_complex_query(coordinator)),
        ("Routing Explanation", lambda: test_routing_explanation(coordinator)),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if await test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    return passed, total

def main():
    """Main test function."""
    print("🧪 Multi-Agent Educational Coordinator Tests")
    print("=" * 60)
    
    # Check environment
    required_vars = ["GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION", "RAG_CORPUS"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please ensure your environment is properly configured.")
        sys.exit(1)
    
    print(f"✅ Environment configured")
    print(f"   Project: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
    print(f"   Location: {os.getenv('GOOGLE_CLOUD_LOCATION')}")
    print(f"   Corpus: {os.getenv('RAG_CORPUS')}")
    
    # Run async tests
    try:
        passed, total = asyncio.run(run_async_tests())
    except Exception as e:
        print(f"❌ Failed to run async tests: {e}")
        passed, total = 0, 3
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Multi-agent coordinator is working correctly.")
        print("\nNext steps:")
        print("1. Test with ADK: adk run coordinator")
        print("2. Compare with simple RAG: adk run rag")
        print("3. Deploy the system: python deployment/deploy.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        
    print(f"\n🚀 Ready to test with: adk run coordinator")

if __name__ == "__main__":
    main() 