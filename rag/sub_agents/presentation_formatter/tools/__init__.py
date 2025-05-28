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

"""Presentation formatter specific tools."""

from .report_formatter import format_comprehensive_report, export_report_sections, get_session_summary, export_to_pdf

# Import global memory and validation tools for comprehensive reporting
from rag.tools.memory import memorize_analysis, forget_analysis, get_session_summary as get_global_session_summary, clear_session_data
from rag.tools.validation import validate_report_card, ensure_data_consistency, get_validation_summary

__all__ = [
    "format_comprehensive_report",
    "export_report_sections",
    "get_session_summary",
    "export_to_pdf",
    # Global memory management
    "memorize_analysis",
    "forget_analysis",
    "get_global_session_summary",
    "clear_session_data",
    # Data validation
    "validate_report_card",
    "ensure_data_consistency",
    "get_validation_summary",
] 