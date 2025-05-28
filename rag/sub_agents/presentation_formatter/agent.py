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

"""Presentation Formatter agent for creating professional educational reports."""

from google.adk.agents import Agent

from rag.sub_agents.presentation_formatter.prompt import PRESENTATION_FORMATTER_INSTR
from rag.sub_agents.presentation_formatter.tools import (
    format_comprehensive_report, 
    export_report_sections, 
    get_session_summary,
    memorize_analysis,
    forget_analysis,
    get_global_session_summary,
    clear_session_data,
    validate_report_card,
    ensure_data_consistency,
    get_validation_summary
)

presentation_formatter_agent = Agent(
    model="gemini-2.0-flash",
    name="presentation_formatter_agent", 
    description="Formats educational analysis into professional, user-friendly reports with memory and validation capabilities",
    instruction=PRESENTATION_FORMATTER_INSTR,
    tools=[
        format_comprehensive_report, 
        export_report_sections, 
        get_session_summary,
        memorize_analysis,
        forget_analysis,
        get_global_session_summary,
        clear_session_data,
        validate_report_card,
        ensure_data_consistency,
        get_validation_summary
    ],
    output_key="formatted_report",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
) 