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

"""Student data extraction and storage tools for data retriever."""

from datetime import datetime
from typing import Dict, Any

from google.adk.tools import ToolContext


def extract_student_info(report_data: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Extract and store key student information from report card data.
    
    Args:
        report_data: Raw report card text or key information
        tool_context: The ADK tool context for state management
        
    Returns:
        Status message with extracted information summary
    """
    # Store the original report data
    tool_context.state["original_report_data"] = report_data
    tool_context.state["analysis_timestamp"] = str(datetime.now())
    
    # Initialize structured storage for analysis
    if "student_profile" not in tool_context.state:
        tool_context.state["student_profile"] = {
            "name": "",
            "grade": "",
            "school": "",
            "subjects": [],
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
    
    # Basic extraction of key info (this could be enhanced with NLP)
    lines = report_data.split('\n')
    for line in lines:
        line = line.strip().lower()
        if 'student:' in line or 'name:' in line:
            tool_context.state["student_profile"]["name"] = line.split(':')[-1].strip()
        elif 'grade:' in line and 'grade level' not in line:
            tool_context.state["student_profile"]["grade"] = line.split(':')[-1].strip()
        elif 'school:' in line:
            tool_context.state["student_profile"]["school"] = line.split(':')[-1].strip()
    
    return {
        "status": f"Extracted student information and stored in session state",
        "timestamp": tool_context.state["analysis_timestamp"],
        "student_name": tool_context.state["student_profile"]["name"]
    }


def store_analysis_results(analysis_type: str, results: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Store analysis results in session state for later retrieval.
    
    Args:
        analysis_type: Type of analysis (data_retrieval, weakness_analysis, solution_research, study_plan, etc.)
        results: The analysis results to store
        tool_context: The ADK tool context for state management
        
    Returns:
        Status message confirming storage
    """
    if "analysis_results" not in tool_context.state:
        tool_context.state["analysis_results"] = {}
    
    tool_context.state["analysis_results"][analysis_type] = {
        "content": results,
        "timestamp": str(datetime.now())
    }
    
    return {
        "status": f"Stored {analysis_type} results in session state",
        "analysis_count": len(tool_context.state["analysis_results"])
    } 