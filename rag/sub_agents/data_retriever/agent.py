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

"""Data Retriever agent for extracting specific information from report cards."""

import os
from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from dotenv import load_dotenv

from rag.sub_agents.data_retriever.prompt import DATA_RETRIEVER_INSTR
from rag.sub_agents.data_retriever.tools import extract_student_info, store_analysis_results

load_dotenv()

# RAG Tool for data retrieval
RAG_CORPUS = os.environ.get("RAG_CORPUS")
if not RAG_CORPUS:
    raise ValueError("RAG_CORPUS environment variable not set.")

report_card_retrieval_tool = VertexAiRagRetrieval(
    name="retrieve_student_report_data",
    description="Retrieves specific factual data from student report cards.",
    rag_resources=[rag.RagResource(rag_corpus=RAG_CORPUS)],
    similarity_top_k=5,
    vector_distance_threshold=0.7,
)

data_retriever_agent = Agent(
    model="gemini-2.0-flash",
    name="data_retriever_agent",
    description="Retrieves specific, factual data points from student report cards",
    instruction=DATA_RETRIEVER_INSTR,
    tools=[report_card_retrieval_tool, extract_student_info, store_analysis_results],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
) 