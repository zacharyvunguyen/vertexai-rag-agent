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

"""Study Planner agent for creating personalized learning plans."""

from google.adk.agents import Agent

from rag.sub_agents.study_planner.prompt import STUDY_PLANNER_INSTR
from rag.sub_agents.study_planner.tools import find_educational_resources, organize_study_schedule, store_study_plan

study_planner_agent = Agent(
    model="gemini-2.0-flash",
    name="study_planner_agent",
    description="Creates personalized study plans based on identified weaknesses and researched solutions",
    instruction=STUDY_PLANNER_INSTR,
    tools=[find_educational_resources, organize_study_schedule, store_study_plan],
    output_key="personalized_plan",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
) 