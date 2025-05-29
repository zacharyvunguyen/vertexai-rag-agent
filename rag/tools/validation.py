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

"""Data validation tools for the RAG system."""

from typing import Dict, Any, List
from google.adk.tools import ToolContext


def validate_report_card(report_text: str, tool_context: ToolContext):
    """
    Validate that the provided text appears to be a Williamson County Schools report card.

    Args:
        report_text: The report card text to validate
        tool_context: The ADK tool context

    Returns:
        Validation results with status and details
    """
    validation_results = {
        "is_valid": False,
        "confidence": 0.0,
        "issues": [],
        "strengths": []
    }
    
    # Required elements for Williamson County Schools report cards
    required_elements = [
        ("Student Name:", "student identification"),
        ("Grade:", "grade level"),
        ("School:", "school identification"),
        ("Teacher:", "teacher information"),
    ]
    
    # Academic subject indicators
    academic_subjects = [
        "Reading", "Mathematics", "Science", "Social Studies", 
        "Language Arts", "Writing", "Math", "ELA"
    ]
    
    # Check for required elements
    found_elements = 0
    for element, description in required_elements:
        if element.lower() in report_text.lower():
            found_elements += 1
            validation_results["strengths"].append(f"Found {description}")
        else:
            validation_results["issues"].append(f"Missing {description}")
    
    # Check for academic subjects
    found_subjects = 0
    for subject in academic_subjects:
        if subject.lower() in report_text.lower():
            found_subjects += 1
    
    if found_subjects > 0:
        validation_results["strengths"].append(f"Found {found_subjects} academic subjects")
    else:
        validation_results["issues"].append("No recognizable academic subjects found")
    
    # Calculate confidence
    element_confidence = found_elements / len(required_elements)
    subject_confidence = min(found_subjects / 3, 1.0)  # Expect at least 3 subjects
    validation_results["confidence"] = (element_confidence + subject_confidence) / 2
    
    # Determine if valid (at least 70% confidence)
    validation_results["is_valid"] = validation_results["confidence"] >= 0.7
    
    # Store validation results in session
    tool_context.state["report_validation"] = validation_results
    
    return validation_results


def ensure_data_consistency(tool_context: ToolContext):
    """
    Check for data consistency across all stored session data.

    Args:
        tool_context: The ADK tool context

    Returns:
        Consistency check results
    """
    consistency_results = {
        "is_consistent": True,
        "issues": [],
        "warnings": []
    }
    
    # Check if student profile exists
    student_profile = tool_context.state.get("student_profile", {})
    if not student_profile:
        consistency_results["issues"].append("No student profile found in session")
        consistency_results["is_consistent"] = False
    else:
        # Check required profile fields
        required_fields = ["name", "grade", "school"]
        for field in required_fields:
            if not student_profile.get(field):
                consistency_results["issues"].append(f"Missing {field} in student profile")
                consistency_results["is_consistent"] = False
    
    # Check analysis results consistency
    analysis_results = tool_context.state.get("analysis_results", {})
    if analysis_results:
        for analysis_type, analysis_data in analysis_results.items():
            if not analysis_data.get("timestamp"):
                consistency_results["warnings"].append(f"Analysis '{analysis_type}' missing timestamp")
            
            if not analysis_data.get("type"):
                consistency_results["warnings"].append(f"Analysis '{analysis_type}' missing type field")
    
    # Check timestamp consistency
    profile_timestamp = tool_context.state.get("analysis_timestamp")
    if analysis_results and not profile_timestamp:
        consistency_results["warnings"].append("Analysis results exist but no global timestamp found")
    
    # Store consistency results
    tool_context.state["data_consistency"] = consistency_results
    
    return consistency_results


def get_validation_summary(tool_context: ToolContext):
    """
    Get a summary of all validation results.

    Args:
        tool_context: The ADK tool context

    Returns:
        Summary of validation and consistency checks
    """
    return {
        "report_validation": tool_context.state.get("report_validation", {}),
        "data_consistency": tool_context.state.get("data_consistency", {}),
        "validation_timestamp": tool_context.state.get("analysis_timestamp", "")
    } 