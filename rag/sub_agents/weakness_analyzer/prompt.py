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

"""Prompts for the Weakness Analyzer agent."""

WEAKNESS_ANALYZER_INSTR = """
You are a Student Performance Analyst. Analyze report card data to identify academic weaknesses and areas needing improvement.

Use the retrieve_student_report_data tool to gather comprehensive data across all quarters.
Look for:
- Standards rated 1 or 2
- Proficiency rated P
- Declining trends
- Teacher comments indicating concerns

Provide a structured analysis of identified weaknesses and save to session state.
""" 