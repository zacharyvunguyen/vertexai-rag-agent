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

"""Weakness Analyzer agent for identifying academic weaknesses from report cards."""

from google.adk.agents import Agent
from rag.sub_agents.weakness_analyzer.prompt import WEAKNESS_ANALYZER_INSTR
from rag.tools.rag_retrieval import rag_retrieval_grounding

weakness_analyzer_agent = Agent(
    model="gemini-2.0-flash",
    name="weakness_analyzer_agent",
    description="Analyzes report card data to identify academic weaknesses and areas needing improvement",
    instruction=WEAKNESS_ANALYZER_INSTR,
    tools=[rag_retrieval_grounding],
    output_key="identified_weaknesses",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
) 