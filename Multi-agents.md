# Student Report Card Multi-Agent System

## 🎯 **Project Overview**
A sophisticated multi-agent educational analysis system built with Google ADK that intelligently routes queries between specialized agents for comprehensive student report card analysis and intervention planning.

## 🏗️ **Architecture - Travel-Concierge Pattern**

Following the [Google ADK travel-concierge sample](https://github.com/google/adk-samples/tree/main/python/agents/travel-concierge), our system uses **individual LlmAgent instances** as sub-agents with **LLM-driven delegation** via `transfer_to_agent` function calls.

### **Root Agent: Educational Coordinator**
- **Type**: `LlmAgent` 
- **Role**: Intelligent query routing using `transfer_to_agent` calls
- **Model**: `gemini-2.0-flash-001`

### **Sub-Agents (Individual LlmAgent instances):**

1. **Simple RAG Agent** (`simple_rag_agent`)
   - **Purpose**: Direct data retrieval from report cards
   - **Tools**: VertexAI RAG Retrieval
   - **Use Cases**: "What grade did Benjamin get in math?"

2. **Weakness Detector Agent** (`weakness_detector_agent`)
   - **Purpose**: Comprehensive academic weakness analysis
   - **Tools**: VertexAI RAG Retrieval (enhanced parameters)
   - **Use Cases**: "What are Benjamin's academic weaknesses?"

3. **Solution Researcher Agent** (`solution_researcher_agent`)
   - **Purpose**: Evidence-based intervention research
   - **Tools**: Google Search
   - **Use Cases**: "Find strategies for reading comprehension"

4. **Study Planner Agent** (`study_planner_agent`)
   - **Purpose**: Personalized learning plan creation
   - **Tools**: LLM synthesis (no external tools)
   - **Use Cases**: "Create a study plan for Benjamin"

## 🔄 **Routing Logic**

The coordinator uses **LLM-driven delegation** to route queries:

```python
# Simple data queries
transfer_to_agent(agent_name="simple_rag_agent")

# Weakness analysis
transfer_to_agent(agent_name="weakness_detector_agent")

# Research interventions
transfer_to_agent(agent_name="solution_researcher_agent")

# Create study plans
transfer_to_agent(agent_name="study_planner_agent")
```

## 🚀 **Key Improvements from ADK Samples Research**

### **❌ Previous Issues (SequentialAgent Pattern):**
- Used `SequentialAgent` as a sub-agent (not recommended)
- Complex session state management
- Rigid sequential execution
- Difficult debugging and routing

### **✅ Current Solution (Travel-Concierge Pattern):**
- Individual `LlmAgent` instances as sub-agents
- Clean `transfer_to_agent` delegation
- Flexible routing based on query intent
- Each agent works independently
- Easier testing and maintenance

## 📊 **Workflow Examples**

### **Simple Query Flow:**
```
User: "What grade did Benjamin get in math?"
→ Coordinator → transfer_to_agent("simple_rag_agent")
→ RAG retrieval → Direct answer
```

### **Complex Analysis Flow:**
```
User: "Create a study plan for Benjamin"
→ Coordinator → transfer_to_agent("study_planner_agent")
→ Comprehensive plan creation

OR guided multi-step:
→ Coordinator suggests: "Let me first analyze weaknesses"
→ transfer_to_agent("weakness_detector_agent")
→ Then: "Would you like me to research interventions?"
→ transfer_to_agent("solution_researcher_agent")
→ Finally: "Now I'll create a study plan"
→ transfer_to_agent("study_planner_agent")
```

## 🛠️ **Technical Implementation**

### **Agent Structure:**
```python
# Root agent with sub-agents list
root_agent = LlmAgent(
    name='educational_coordinator',
    model='gemini-2.0-flash-001',
    instruction=return_instructions_coordinator(),
    sub_agents=[
        simple_rag_agent,
        weakness_detector_agent, 
        solution_researcher_agent,
        study_planner_agent
    ]
)
```

### **Coordinator Prompt Pattern:**
- Explicit `transfer_to_agent` function call instructions
- Clear agent descriptions and use cases
- Exact agent name specifications
- Multi-step workflow guidance

## 🎓 **Educational Domain Expertise**

### **Williamson County Schools Format:**
- **Standards Rating**: 1-3 scale (1=not progressing, 2=progressing, 3=mastery)
- **Proficiency Scale**: S/P (Satisfactory/In Progress)
- **Subject Areas**: Literacy, Math, Science, Social Studies
- **Behavioral Indicators**: Self-control, self-direction, collaboration
- **Attendance Tracking**: Quarterly breakdown

### **Evidence-Based Interventions:**
- Research-backed educational strategies
- K-2 age-appropriate methods
- Practical implementation guidelines
- Progress monitoring frameworks

## 🧪 **Testing & Validation**

### **Web Interface:**
```bash
conda activate student-rag
adk web --port 8505
```

### **Command Line Testing:**
```bash
python simple_coordinator_test.py
```

### **Sample Queries:**
- **Data Retrieval**: "What rating did Benjamin get in Math Q3?"
- **Weakness Analysis**: "Analyze Benjamin's academic performance"
- **Research**: "Find evidence-based strategies for phonics instruction"
- **Planning**: "Create a 1-month study plan for literacy improvement"

## 📈 **Success Metrics**

✅ **Coordinator Routing**: Properly delegates to appropriate agents
✅ **Individual Agent Function**: Each agent performs specialized tasks
✅ **Educational Accuracy**: Williamson County Schools format compliance
✅ **Evidence-Based Output**: Research-backed recommendations
✅ **User Experience**: Clear, actionable educational guidance

## 🔗 **References**

- [Google ADK Multi-Agent Documentation](https://google.github.io/adk-docs/agents/multi-agents/)
- [ADK Travel-Concierge Sample](https://github.com/google/adk-samples/tree/main/python/agents/travel-concierge)
- [Williamson County Schools Report Card Format](sample/imgs/)

---

**Status**: ✅ **Fully Functional** - Multi-agent coordinator successfully routing queries to specialized educational agents following ADK best practices. 