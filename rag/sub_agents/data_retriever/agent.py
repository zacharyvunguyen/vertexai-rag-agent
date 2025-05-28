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

from google.adk.agents import Agent
from rag.sub_agents.data_retriever.prompt import DATA_RETRIEVER_INSTR
from rag.sub_agents.data_retriever.tools import extract_student_info, store_analysis_results
from rag.tools.rag_retrieval import rag_retrieval_grounding

data_retriever_agent = Agent(
    model="gemini-2.0-flash",
    name="data_retriever_agent",
    description="Retrieves specific, factual data points from student report cards",
    instruction=DATA_RETRIEVER_INSTR,
    tools=[rag_retrieval_grounding, extract_student_info, store_analysis_results],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
) 