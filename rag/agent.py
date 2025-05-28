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

"""Student Report Card RAG Multi-Agent System following ADK best practices."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from rag import prompt
from rag.sub_agents.data_retriever.agent import data_retriever_agent
from rag.sub_agents.weakness_analyzer.agent import weakness_analyzer_agent
from rag.sub_agents.solution_researcher.agent import solution_researcher_agent
from rag.sub_agents.study_planner.agent import study_planner_agent
from rag.sub_agents.presentation_formatter.agent import presentation_formatter_agent

root_agent = Agent(
    model="gemini-2.0-flash",
    name="root_agent",
    description="Educational Analysis Coordinator that helps analyze student report cards and create improvement plans",
    instruction=prompt.ROOT_AGENT_INSTR,
    tools=[
        AgentTool(agent=data_retriever_agent),
        AgentTool(agent=weakness_analyzer_agent),
        AgentTool(agent=solution_researcher_agent),
        AgentTool(agent=study_planner_agent),
        AgentTool(agent=presentation_formatter_agent),
    ],
)

# Note: The `adk_config.yaml` should point to this `root_agent`.
# Example adk_config.yaml:
# agents:
#   rag:
#     name: "Student Report Card Multi-Agent System"
#     module: "rag"
#     agent_name: "root_agent"
#     type: "conversational"