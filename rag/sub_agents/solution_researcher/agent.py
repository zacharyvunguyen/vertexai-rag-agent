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

"""Solution Researcher agent for finding educational interventions and strategies."""

from google.adk.agents import Agent
from google.adk.tools import google_search

from rag.sub_agents.solution_researcher.prompt import SOLUTION_RESEARCHER_INSTR

solution_researcher_agent = Agent(
    model="gemini-2.0-flash",
    name="solution_researcher_agent",
    description="Researches evidence-based strategies and resources for educational challenges",
    instruction=SOLUTION_RESEARCHER_INSTR,
    tools=[google_search],
    output_key="research_findings",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
) 