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

"""Educational resource discovery and organization tools for study planner."""

from datetime import datetime
from typing import Dict, Any, List
from google.adk.tools import ToolContext


def find_educational_resources(subject: str, grade_level: str, resource_type: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Find and organize educational resources based on subject, grade level, and type.
    
    Args:
        subject: Subject area (math, reading, science, etc.)
        grade_level: Student's grade level
        resource_type: Type of resource (practice_worksheets, video_tutorials, interactive_games, etc.)
        tool_context: The ADK tool context for state management
        
    Returns:
        Organized educational resources with recommendations
    """
    # Initialize resources storage if not exists
    if "educational_resources" not in tool_context.state:
        tool_context.state["educational_resources"] = {}
    
    resource_key = f"{subject}_{grade_level}_{resource_type}"
    
    # Predefined educational resource templates (in a real system, this would query external APIs)
    resource_templates = {
        "math": {
            "practice_worksheets": [
                "Khan Academy Math Practice Worksheets",
                "IXL Math Skills Practice",
                "Math-Drills.com Worksheets",
                "Education.com Math Practice Sheets"
            ],
            "video_tutorials": [
                "Khan Academy Math Videos",
                "Professor Leonard Math Tutorials", 
                "Math Antics Video Series",
                "Numberphile Educational Videos"
            ],
            "interactive_games": [
                "Prodigy Math Game",
                "Sumdog Math Games",
                "Math Playground Interactive Activities",
                "Cool Math Games Educational Section"
            ]
        },
        "reading": {
            "practice_worksheets": [
                "Reading Comprehension Worksheets by grade",
                "Scholastic Reading Practice Sheets",
                "K5 Learning Reading Worksheets",
                "Super Teacher Worksheets Reading"
            ],
            "video_tutorials": [
                "Reading Strategies Video Lessons",
                "Phonics and Decoding Video Tutorials",
                "Comprehension Strategy Videos",
                "Guided Reading Video Sessions"
            ],
            "interactive_games": [
                "Epic! Digital Library Games",
                "Reading Eggs Interactive Activities",
                "Starfall Reading Games",
                "ABCmouse Reading Activities"
            ]
        },
        "science": {
            "practice_worksheets": [
                "Science experiment worksheets",
                "Bill Nye Science Worksheets",
                "NASA Educational Activity Sheets",
                "National Geographic Kids Science Worksheets"
            ],
            "video_tutorials": [
                "Crash Course Science Videos",
                "Bill Nye the Science Guy Episodes",
                "SciShow Kids Educational Videos",
                "NASA STEM Video Series"
            ],
            "interactive_games": [
                "BrainPOP Science Games",
                "NASA Kids Club Interactive Activities",
                "Science4Us Digital Activities",
                "Mystery Science Interactive Lessons"
            ]
        }
    }
    
    # Get resources for the specified subject and type
    subject_lower = subject.lower()
    resources = []
    
    if subject_lower in resource_templates and resource_type in resource_templates[subject_lower]:
        resources = resource_templates[subject_lower][resource_type]
    
    # Add grade-specific customization
    grade_specific_notes = {
        "elementary": "Focus on foundational skills and visual learning",
        "middle": "Include analytical thinking and problem-solving approaches",
        "high": "Emphasize critical thinking and advanced concepts"
    }
    
    grade_category = "elementary" if grade_level in ["K", "1", "2", "3", "4", "5"] else \
                    "middle" if grade_level in ["6", "7", "8"] else "high"
    
    # Store resources in session state
    tool_context.state["educational_resources"][resource_key] = {
        "subject": subject,
        "grade_level": grade_level,
        "resource_type": resource_type,
        "resources": resources,
        "grade_notes": grade_specific_notes.get(grade_category, ""),
        "recommended_count": len(resources)
    }
    
    return {
        "subject": subject,
        "grade_level": grade_level,
        "resource_type": resource_type,
        "found_resources": resources,
        "grade_specific_guidance": grade_specific_notes.get(grade_category, ""),
        "status": f"Found {len(resources)} {resource_type} resources for {subject} at grade {grade_level}",
        "storage_key": resource_key
    }


def organize_study_schedule(resources_list: List[str], study_duration_weeks: int, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Organize educational resources into a structured study schedule.
    
    Args:
        resources_list: List of educational resources to organize
        study_duration_weeks: Number of weeks for the study schedule
        tool_context: The ADK tool context for state management
        
    Returns:
        Organized study schedule with resource allocation
    """
    if study_duration_weeks < 1:
        study_duration_weeks = 4  # Default to 4 weeks
    
    # Calculate resources per week
    resources_per_week = max(1, len(resources_list) // study_duration_weeks)
    
    # Create weekly schedule
    weekly_schedule = {}
    resource_index = 0
    
    for week in range(1, study_duration_weeks + 1):
        week_resources = []
        for i in range(resources_per_week):
            if resource_index < len(resources_list):
                week_resources.append(resources_list[resource_index])
                resource_index += 1
        
        # Add any remaining resources to the last week
        if week == study_duration_weeks:
            while resource_index < len(resources_list):
                week_resources.append(resources_list[resource_index])
                resource_index += 1
        
        weekly_schedule[f"Week {week}"] = {
            "resources": week_resources,
            "focus_areas": f"Complete {len(week_resources)} learning activities",
            "time_allocation": "15-30 minutes per resource"
        }
    
    # Store schedule in session state
    tool_context.state["study_schedule"] = {
        "total_weeks": study_duration_weeks,
        "total_resources": len(resources_list),
        "weekly_breakdown": weekly_schedule,
        "created_at": str(dict(tool_context.state).get("analysis_timestamp", ""))
    }
    
    return {
        "study_schedule": weekly_schedule,
        "total_duration": f"{study_duration_weeks} weeks",
        "resources_organized": len(resources_list),
        "status": f"Created {study_duration_weeks}-week study schedule with {len(resources_list)} resources"
    }


def store_study_plan(plan_content: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Store the finalized study plan in session state.
    
    Args:
        plan_content: The complete study plan content
        tool_context: The ADK tool context for state management
        
    Returns:
        Status message confirming storage
    """
    if "analysis_results" not in tool_context.state:
        tool_context.state["analysis_results"] = {}
    
    tool_context.state["analysis_results"]["study_plan"] = {
        "content": plan_content,
        "timestamp": str(datetime.now())
    }
    
    return {
        "status": "Study plan stored in session state",
        "analysis_count": len(tool_context.state["analysis_results"])
    } 