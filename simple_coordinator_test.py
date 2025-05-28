#!/usr/bin/env python3
"""
Simple test to verify coordinator routing works.
Based on our working test_rag_agent.py pattern.
"""

from rag.agent import root_agent

def test_simple_routing():
    """Simple test of coordinator routing."""
    
    print("🧪 Testing Coordinator Routing...")
    print("=" * 50)
    
    # Test queries
    queries = [
        "What grade did Benjamin get in math?",  # Should route to simple_rag_agent
        "Create a study plan for Benjamin"       # Should route to educational_pipeline
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 30)
        
        try:
            # Use run_live like the working test_rag_agent.py
            response = root_agent.run_live(query)
            print(f"📋 Response: {response}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            
        print("\n" + "="*50)

if __name__ == "__main__":
    test_simple_routing() 