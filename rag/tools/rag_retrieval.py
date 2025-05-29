# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrapper for RAG retrieval with custom prompt for student report cards."""

import os
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from dotenv import load_dotenv

load_dotenv()

# Set up RAG tool
RAG_CORPUS = os.environ.get("RAG_CORPUS")
if not RAG_CORPUS:
    raise ValueError("RAG_CORPUS environment variable not set.")

report_card_retrieval_tool = VertexAiRagRetrieval(
    name="retrieve_student_report_data",
    description="Retrieves comprehensive report card data for analysis.",
    rag_resources=[rag.RagResource(rag_corpus=RAG_CORPUS)],
    similarity_top_k=5,
    vector_distance_threshold=0.7,
)

_rag_agent = Agent(
    model="gemini-2.0-flash",
    name="rag_retrieval_grounding",
    description="An agent providing RAG retrieval capability for student report cards",
    instruction="""
    Use the retrieve_student_report_data tool to find information about students from Williamson County Schools report cards.
    
    Format your response to include:
    - Student name, grade, and school
    - Relevant performance data for the requested subject area
    - Specific scores, ratings, or assessments
    - Quarter-by-quarter trends if available
    
    Be specific and cite the data source. If no data is found for the requested student, clearly state this.
    """,
    tools=[report_card_retrieval_tool],
)

rag_retrieval_grounding = AgentTool(agent=_rag_agent) 