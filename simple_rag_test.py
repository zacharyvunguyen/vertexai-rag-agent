#!/usr/bin/env python3
"""
Simple test for the Student Report Card RAG Agent
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("🧪 Simple RAG Agent Test")
    print("=" * 40)
    
    # Import the agent
    try:
        from rag.agent import root_agent
        print("✅ Agent imported successfully")
        print(f"   Agent name: {root_agent.name}")
        print(f"   Tools available: {[tool.name for tool in root_agent.tools]}")
    except Exception as e:
        print(f"❌ Failed to import agent: {e}")
        return
    
    # Test a simple query
    print("\n🔍 Testing with a simple query...")
    query = "Hello, can you help me analyze student performance data?"
    print(f"Query: {query}")
    
    try:
        # Try using run_live method
        response = root_agent.run_live(query)
        print(f"\n💬 Response: {response}")
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Try to get more details about the agent
        print(f"\n🔍 Agent details:")
        print(f"   Model: {root_agent.model}")
        print(f"   Available methods: {[m for m in dir(root_agent) if not m.startswith('_') and callable(getattr(root_agent, m))]}")

if __name__ == "__main__":
    main() 