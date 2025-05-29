# Sample Test Questions for Student Report Card RAG System

This document provides comprehensive test questions for the multi-agent Student Report Card RAG system, organized by complexity and expected agent routing behavior.

## 🎯 Quick Start Test Suite

### Essential Tests (Run These First)
1. **Simple Data Retrieval**: "What rating did Benjamin get in Math counting for Q3?"
2. **Complex Analysis**: "Create a study plan for Benjamin's weak areas"
3. **Routing Test**: "Benjamin's attendance numbers" vs "Help Benjamin improve academically"

---

## 📊 Simple RAG Agent Tests (Direct Data Retrieval)
*Expected: Fast responses (2-3 seconds) from simple_rag_agent*

### Basic Performance Queries
1. "What rating did Benjamin get in Math counting for Q3?"
2. "Show me Benjamin's literacy scores for all quarters"
3. "What is Benjamin's rating in self-control?"
4. "How many days was Benjamin absent this year?"
5. "What did the teacher say in the Q2 comments?"
6. "Display Benjamin's science grades for plant life cycles"
7. "What's Benjamin's attendance pattern across all quarters?"
8. "Show me the proficiency ratings for Art and Music"

### Specific Standards Questions
9. "What rating did Benjamin receive for CVC patterns in literacy?"
10. "How is Benjamin doing with number recognition in math?"
11. "What's Benjamin's rating for working with others?"
12. "Show me Benjamin's geometric shapes understanding score"
13. "What rating did Benjamin get for following directions?"
14. "Display Benjamin's self-directed learning ratings"
15. "What's Benjamin's proficiency in Physical Education?"

### Quarterly Comparison Questions
16. "Did Benjamin's math scores improve from Q1 to Q3?"
17. "Compare Benjamin's literacy ratings across all quarters"
18. "Show me the trend in Benjamin's self-directed learning ratings"
19. "What's the pattern in Benjamin's attendance across quarters?"
20. "How did Benjamin's science ratings change over the year?"

---

## 🔬 Educational Pipeline Tests (Complex Analysis & Intervention)
*Expected: Comprehensive responses (10-15 seconds) with research and planning*

### Weakness Analysis & Study Plans
21. "Create a study plan for Benjamin's weak areas"
22. "How can we help Benjamin improve in math?"
23. "Analyze Benjamin's weakness patterns and recommend solutions"
24. "Develop an intervention plan for Benjamin's literacy struggles"
25. "What strategies would help with Benjamin's behavioral issues?"
26. "Create a personalized learning plan based on Benjamin's report card"

### Comprehensive Educational Analysis
27. "What educational resources would benefit Benjamin most?"
28. "Design a home support plan for Benjamin's parents"
29. "Create a 6-week improvement plan for Benjamin's lowest-rated areas"
30. "What evidence-based interventions would help Benjamin's specific needs?"
31. "Develop strategies to improve Benjamin's self-control and focus"
32. "Create an academic support plan for Benjamin's struggling subjects"

### Research-Based Intervention Planning
33. "Find proven methods to help first-graders with counting difficulties"
34. "What research supports helping students with CVC pattern recognition?"
35. "Create an evidence-based plan for improving classroom behavior"
36. "Research effective interventions for first-grade writing skills"

---

## 🧭 Coordinator Intelligence Tests
*Testing smart routing between simple RAG and educational pipeline*

### Should Route to Simple RAG
37. "Benjamin's Q1 math rating"
38. "What are Benjamin's attendance numbers?"
39. "Show me the teacher comments for Q3"
40. "Benjamin's proficiency in Art class"
41. "What rating did Benjamin get for working with others?"

### Should Route to Educational Pipeline
42. "Help Benjamin succeed in first grade"
43. "Create strategies to improve Benjamin's academic performance"
44. "How can we support Benjamin's learning at home?"
45. "Develop an intervention plan for Benjamin"
46. "What can we do about Benjamin's struggling areas?"

---

## 🔄 Multi-Agent Workflow Tests
*Testing session state, tool usage, and agent coordination*

### Full Pipeline Integration Tests
47. "Identify Benjamin's academic weaknesses and create an evidence-based improvement plan"
   - **Tests**: Weakness detection → Google Search research → Study plan creation → Professional formatting
   - **Verifies**: Session state passing, Google Search tool usage, comprehensive planning, beautiful report output

48. "What areas need intervention and what research supports helping students like Benjamin?"
   - **Tests**: Full pipeline with research integration and professional presentation
   - **Verifies**: Tool coordination, research findings integration, formatted output

49. "Analyze Benjamin's report card and provide research-backed recommendations"
   - **Tests**: Complete educational analysis workflow with presentation formatting
   - **Verifies**: Multi-agent collaboration, evidence-based planning, and professional report generation

### Session State Verification Tests
50. "Find Benjamin's weaknesses, research solutions, and create a study plan"
51. "What are Benjamin's problem areas and how can research help address them?"
52. "Create a comprehensive intervention strategy based on Benjamin's performance data"

### Presentation & Export Tests
53. "Generate a professional report for Benjamin's educational analysis"
   - **Tests**: Full pipeline with beautiful formatting and PDF export capability
   - **Verifies**: Presentation formatter agent, professional output, export functionality

54. "Create a parent-friendly report about Benjamin's academic progress"
   - **Tests**: Technical analysis transformed into accessible format
   - **Verifies**: Language translation, visual formatting, stakeholder-appropriate content

55. "Develop a comprehensive educational report suitable for teacher conferences"
   - **Tests**: Professional formatting for educational meetings
   - **Verifies**: Conference-ready output, actionable recommendations, professional presentation

---

## ⚠️ Edge Cases & Error Handling

### Data Boundary Tests
56. "What was Benjamin's rating in Q5?" *(invalid quarter)*
57. "Show me Benjamin's college readiness scores" *(inappropriate for grade level)*
58. "What rating did Sarah get in math?" *(different student name)*
59. "Display Benjamin's AP test scores" *(not applicable to first grade)*

### Complex Interpretation Tests
60. "Is Benjamin meeting grade-level expectations overall?"
61. "What does a rating of 2 in literacy mean for Benjamin's development?"
62. "Should we be concerned about Benjamin's progress patterns?"
63. "How does Benjamin compare to typical first-grade students?"

---

## ⚡ Performance & Efficiency Tests

### Speed Comparison Tests
64. "Benjamin's math Q2 rating" *(should be fast - simple RAG)*
65. "Comprehensive academic analysis for Benjamin" *(should be thorough - full pipeline)*
66. "Quick lookup: Benjamin's science rating" *(simple RAG)*
67. "Detailed intervention planning for Benjamin" *(educational pipeline)*

---

## 🔗 Integration Tests

### Cross-Subject Analysis
68. "How do Benjamin's behavioral ratings correlate with his academic performance?"
69. "Does Benjamin's attendance impact his learning outcomes?"
70. "What patterns do you see across Benjamin's academic and social development?"
71. "Analyze the relationship between Benjamin's self-control and academic success"

### Holistic Assessment Questions
72. "Provide a complete picture of Benjamin's first-grade experience"
73. "What story does Benjamin's report card tell about his learning journey?"
74. "Create a comprehensive profile of Benjamin as a learner"

---

## 🧪 Advanced Testing Scenarios

### Multi-Turn Conversations
75. Start with: "What are Benjamin's math ratings?"
    Follow up: "Now create an improvement plan for those areas"

76. Start with: "Show me Benjamin's weakest subjects"
    Follow up: "Research interventions for those specific areas"

### Context Switching Tests
77. "Benjamin's Q1 literacy score" → "Create a reading intervention plan"
78. "Teacher comments for Q2" → "Address the concerns mentioned in those comments"

---

## 📋 Testing Checklist

### ✅ Functional Tests
- [ ] Simple RAG queries return data quickly (2-3 seconds)
- [ ] Educational pipeline executes full workflow (10-15 seconds)
- [ ] Coordinator routes queries correctly
- [ ] Google Search tool is called during research phase
- [ ] Session state passes data between agents
- [ ] Weakness detection identifies actual issues
- [ ] Research findings are evidence-based and relevant
- [ ] Study plans are actionable and age-appropriate

### ✅ Quality Tests
- [ ] Responses are accurate to Williamson County Schools format
- [ ] Privacy is maintained (student name handling)
- [ ] Language is appropriate for educational context
- [ ] Recommendations are evidence-based
- [ ] Plans are realistic and implementable

### ✅ Performance Tests
- [ ] Simple queries complete under 5 seconds
- [ ] Complex analyses complete under 20 seconds
- [ ] System handles multiple concurrent requests
- [ ] Error handling works for invalid queries

---

## 🎯 Recommended Testing Sequence

1. **Start Simple** (Questions 1-8): Verify basic RAG functionality
2. **Test Routing** (Questions 37-46): Ensure coordinator intelligence
3. **Validate Pipeline** (Questions 21-32, 47-49): Confirm multi-agent workflow
4. **Check Tools** (Questions 47-52): Monitor Google Search usage
5. **Edge Cases** (Questions 53-63): Test error handling
6. **Integration** (Questions 68-74): Verify cross-functional analysis

---

## 💡 Expected Behaviors

### Simple RAG Agent
- **Response Time**: 2-3 seconds
- **Data Source**: Direct RAG retrieval from report card corpus
- **Output**: Specific data points, ratings, comments

### Educational Pipeline
- **Response Time**: 10-15 seconds
- **Process**: Weakness Detection → Research → Planning
- **Tools Used**: VertexAI RAG + Google Search + LLM synthesis
- **Output**: Comprehensive intervention plans with research backing

### Coordinator Agent
- **Decision Making**: Routes based on query intent analysis
- **Simple Routing**: Data requests → simple_rag_agent
- **Complex Routing**: Analysis/planning requests → educational_pipeline

---

## 🔧 Troubleshooting Guide

### If Simple Queries Are Slow
- Check RAG corpus connection
- Verify VertexAI RAG configuration
- Review similarity threshold settings

### If Pipeline Doesn't Use Google Search
- Check google_search tool import
- Verify solution researcher prompt instructions
- Monitor session state data flow

### If Routing Is Incorrect
- Review coordinator prompt logic
- Test with clear simple vs complex queries
- Check transfer_to_agent functionality

---

*Last Updated: January 2025*
*Compatible with: Google ADK Multi-Agent Architecture* 