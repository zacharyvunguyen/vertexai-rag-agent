# Multi-Agent Educational System Design

## Overview

Implementation of an intelligent multi-agent system for student report card analysis using the **Coordinator/Dispatcher Pattern** from ADK. This system provides smart routing between simple RAG queries and comprehensive educational analysis workflows.

## Problem Statement

**Challenge**: Avoid executing the entire educational analysis pipeline for simple RAG questions.

**Solution**: Implement a coordinator agent that intelligently routes queries to appropriate specialist agents based on intent analysis.

## Architecture Pattern

Using ADK's **Coordinator/Dispatcher Pattern** as documented in the [ADK Multi-Agent Systems guide](https://google.github.io/adk-docs/agents/multi-agents/#coordinatordispatcher-pattern).

### Core Components

```
Educational Coordinator (Router)
├── Simple RAG Agent (Fast queries)
└── Educational Pipeline (Complex analysis)
    ├── Weakness Detector Agent
    ├── Solution Researcher Agent
    └── Study Plan Creator Agent
```

## Agent Specifications

### 1. Educational Coordinator
- **Role**: Intelligent query router using LLM-driven delegation
- **Model**: `gemini-2.0-flash-001`
- **Function**: Analyzes user intent and routes to appropriate agent
- **Routing Logic**:
  - **Simple queries** → Transfer to `simple_rag_agent`
  - **Complex analysis** → Transfer to `educational_pipeline`

### 2. Simple RAG Agent
- **Purpose**: Direct access to report card data
- **Tools**: VertexAI RAG Retrieval
- **Use Cases**:
  - "What are John's math grades?"
  - "Show me reading assessment scores"
  - "What did teachers say about behavior?"

### 3. Educational Pipeline (Sequential)
- **Pattern**: Sequential Pipeline using `SequentialAgent`
- **Shared State**: Uses `session.state` for data flow between agents
- **Components**:

#### 3.1 Weakness Detector Agent
- **Input**: Student report card data
- **Tool**: VertexAI RAG Retrieval (comprehensive analysis)
- **Output**: `identified_weaknesses` → state
- **Function**: Identifies academic gaps, performance trends, behavioral concerns

#### 3.2 Solution Researcher Agent
- **Input**: `identified_weaknesses` from state
- **Tool**: Google Search (evidence-based interventions)
- **Output**: `research_findings` → state
- **Function**: Researches proven educational strategies and resources

#### 3.3 Study Plan Creator Agent
- **Input**: `identified_weaknesses` + `research_findings` from state
- **Tool**: LLM synthesis (no external tools)
- **Output**: `personalized_plan` → state
- **Function**: Creates actionable, personalized study plans

## Query Routing Logic

### Route to Simple RAG
```
Patterns: Direct data requests
Examples:
- "What grade did Sarah get in math?"
- "Display the report card summary"
- "What did teachers say about reading progress?"
- "Show me standardized test scores"
```

### Route to Full Pipeline
```
Patterns: Analysis and intervention requests
Examples:
- "How can this student improve in math?"
- "Create a study plan for Sarah"
- "What areas need the most attention?"
- "Develop an academic improvement plan"
```

## Technical Implementation

### ADK Configuration
```yaml
project_name: "student-report-card-rag"
agents:
  coordinator:
    name: "Educational Coordinator"
    description: "AI coordinator that intelligently routes educational queries"
    module: "rag"
    agent_name: "educational_coordinator"
    type: "conversational"
```

### Key ADK Primitives Used

1. **Agent Hierarchy**: Parent-child relationships with sub_agents
2. **LLM-Driven Delegation**: `transfer_to_agent` for intelligent routing
3. **Shared Session State**: `session.state` for data flow in pipeline
4. **Sequential Workflow**: `SequentialAgent` for ordered execution

### File Structure
```
rag/
├── agent.py                 # Original simple RAG agent
├── educational_coordinator.py # New coordinator implementation
├── prompts.py               # All agent instructions
└── __init__.py             # Module exports
```

## User Experience

### Simple Query Flow
```
User: "What are John's math grades?"
↓
Coordinator: "Routing to simple RAG for direct data access"
↓
Simple RAG: [Fast retrieval] → "John received B+ in Math..."
```

### Complex Analysis Flow
```
User: "Help John improve his math performance"
↓
Coordinator: "Routing to educational pipeline for comprehensive analysis"
↓
Pipeline: Weakness Detection → Solution Research → Study Planning
↓
Result: Complete intervention plan with specific strategies
```

## Benefits

### Performance Optimization
- **Fast Simple Queries**: 2-3 seconds for direct data access
- **Comprehensive Analysis**: 10-15 seconds for full pipeline
- **No Unnecessary Processing**: Simple questions skip research/planning

### User Experience
- **Transparent Routing**: Users see why queries are routed
- **Appropriate Responses**: Right level of detail for each query type
- **Flexible Conversations**: Can handle mixed simple/complex queries

### Maintainability
- **Modular Design**: Each agent has single responsibility
- **Easy Extension**: Add new specialist agents without affecting routing
- **Clear Separation**: Simple vs complex logic isolated

## Implementation Phases

### Phase 1: Core Coordinator ✅ (Current)
- [x] Design architecture
- [x] Plan routing logic
- [x] Document specifications

### Phase 2: Implementation (Next)
- [ ] Create coordinator agent with routing prompts
- [ ] Implement educational pipeline with sequential agents
- [ ] Add specialized agent instructions
- [ ] Update ADK configuration

### Phase 3: Testing & Refinement
- [ ] Test routing accuracy with sample queries
- [ ] Optimize agent instructions
- [ ] Performance testing and tuning
- [ ] User experience validation

### Phase 4: Advanced Features
- [ ] Add more specialist agents (homework helper, parent communication)
- [ ] Implement feedback loops and learning
- [ ] Add human-in-the-loop patterns for sensitive decisions

## Success Metrics

- **Routing Accuracy**: >95% correct intent classification
- **Performance**: Simple queries <3s, complex analysis <15s
- **User Satisfaction**: Appropriate response depth for query type
- **System Reliability**: Graceful handling of edge cases

## References

- [ADK Multi-Agent Systems Documentation](https://google.github.io/adk-docs/agents/multi-agents/#coordinatordispatcher-pattern)
- [ADK Coordinator/Dispatcher Pattern](https://google.github.io/adk-docs/agents/multi-agents/#coordinatordispatcher-pattern)
- [ADK Sequential Agents](https://google.github.io/adk-docs/agents/workflow-agents/#sequential-agents) 