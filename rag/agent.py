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

import os

from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

from dotenv import load_dotenv
from .prompts import return_instructions_root

load_dotenv()

ask_vertex_retrieval = VertexAiRagRetrieval(
    name='retrieve_student_report_data',
    description=(
        'Use this tool to retrieve student report card data, academic performance information, '
        'grades, assessments, and educational progress details from the student report card corpus. '
        'This tool provides access to specific student performance data, teacher feedback, '
        'learning objectives progress, and academic standards assessments.'
    ),
    rag_resources=[
        rag.RagResource(
            # Uses the student report card corpus from environment
            rag_corpus=os.environ.get("RAG_CORPUS")
        )
    ],
    similarity_top_k=5,
    vector_distance_threshold=0.7,
)

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='student_report_card_agent',
    instruction=return_instructions_root(),
    tools=[
        ask_vertex_retrieval,
    ]
)