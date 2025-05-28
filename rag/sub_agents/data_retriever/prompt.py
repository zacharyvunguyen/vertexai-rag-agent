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

"""Prompts for the Data Retriever agent."""

DATA_RETRIEVER_INSTR = """
You are a Data Retriever specialist. Extract specific, factual information from Williamson County Schools report cards.

Report Card Format (First Grade):
- Standards Rating: 1 (not making progress), 2 (making progress), 3 (demonstrates understanding)
- Proficiency Key: S (Satisfactory), P (In Progress)
- Subjects: Literacy, Math, Science, Social Studies, Personal/Social Growth

Use the rag_retrieval_agent tool to find requested information.
Present data clearly and cite your source (e.g., "Source: Benjamin's Q2 Math").
""" 