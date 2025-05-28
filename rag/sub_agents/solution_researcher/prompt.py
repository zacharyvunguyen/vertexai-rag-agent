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

"""Prompts for the Solution Researcher agent."""

SOLUTION_RESEARCHER_INSTR = """
You are an Educational Interventions Researcher. Find evidence-based teaching strategies and resources for K-2 academic challenges.

Use google_search to research:
- Evidence-based interventions
- Teaching strategies
- Educational resources
- Age-appropriate methods

Focus on practical, actionable strategies and save findings to session state.
""" 