#!/usr/bin/env python3
"""
Test script to verify coordinator routing with LLM-driven delegation.
Based on ADK Multi-Agent documentation patterns.
"""

import asyncio
import os
import uuid
from dotenv import load_dotenv
from rag.agent import root_agent
from google.adk.sessions import Session
from google.adk.agents.invocation_context import InvocationContext

# Load environment variables
load_dotenv()

async def test_coordinator_routing():
    """Test that coordinator properly routes queries using transfer_to_agent calls."""
    
    print("🧪 Testing Educational Coordinator Routing...")
    print("=" * 50)
    
    # Test cases based on ADK documentation patterns
    test_queries = [
        {
            "query": "What grade did Benjamin get in math?",
            "expected_route": "simple_rag_agent",
            "type": "Data Retrieval"
        },
        {
            "query": "Create a study plan for Benjamin",
            "expected_route": "educational_pipeline", 
            "type": "Analysis & Planning"
        },
        {
            "query": "How can Benjamin improve his reading skills?",
            "expected_route": "educational_pipeline",
            "type": "Analysis & Planning"
        }
    ]
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {test['type']}")
        print(f"Query: '{test['query']}'")
        print(f"Expected Route: {test['expected_route']}")
        print("-" * 30)
        
        try:
            # Create a proper session and context with required fields
            session = Session(
                id=str(uuid.uuid4()),
                app_name="student-report-card-rag",
                user_id="test-user"
            )
            context = InvocationContext(
                session=session,
                agent=root_agent,
                user_message=test['query']
            )
            
            # Test the coordinator's routing decision
            response_generator = root_agent.run_async(context)
            
            # Print the response to see routing behavior
            print("📋 Coordinator Response:")
            async for event in response_generator:
                if hasattr(event, 'content') and event.content:
                    print(f"  Content: {event.content}")
                if hasattr(event, 'author'):
                    print(f"  Author: {event.author}")
                if hasattr(event, 'actions') and event.actions:
                    print(f"  Actions: {event.actions}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            
        print("\n" + "="*50)

if __name__ == "__main__":
    asyncio.run(test_coordinator_routing()) 