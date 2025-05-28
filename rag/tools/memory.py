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

"""Memory and session state management tools for the RAG system."""

from datetime import datetime
import json
import os
from typing import Dict, Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

# Constants for session state keys
STUDENT_PROFILE_KEY = "student_profile"
ANALYSIS_RESULTS_KEY = "analysis_results"
ANALYSIS_TIMESTAMP_KEY = "analysis_timestamp"
RAG_INITIALIZED_KEY = "rag_initialized"
SYSTEM_TIME_KEY = "system_time"

SAMPLE_PROFILE_PATH = os.getenv(
    "RAG_SAMPLE_PROFILE", "sample/sample_student_profile.json"
)


def memorize_analysis(analysis_type: str, analysis_data: Dict[str, Any], tool_context: ToolContext):
    """
    Store analysis results in session memory.

    Args:
        analysis_type: Type of analysis (e.g., 'weakness_analysis', 'study_plan')
        analysis_data: The analysis data to store
        tool_context: The ADK tool context

    Returns:
        A status message
    """
    if ANALYSIS_RESULTS_KEY not in tool_context.state:
        tool_context.state[ANALYSIS_RESULTS_KEY] = {}
    
    tool_context.state[ANALYSIS_RESULTS_KEY][analysis_type] = {
        **analysis_data,
        "timestamp": str(datetime.now()),
        "type": analysis_type
    }
    
    return {"status": f'Stored analysis "{analysis_type}" with {len(analysis_data)} data points'}


def forget_analysis(analysis_type: str, tool_context: ToolContext):
    """
    Remove specific analysis from session memory.

    Args:
        analysis_type: Type of analysis to remove
        tool_context: The ADK tool context

    Returns:
        A status message
    """
    if ANALYSIS_RESULTS_KEY in tool_context.state and analysis_type in tool_context.state[ANALYSIS_RESULTS_KEY]:
        del tool_context.state[ANALYSIS_RESULTS_KEY][analysis_type]
        return {"status": f'Removed analysis "{analysis_type}"'}
    
    return {"status": f'Analysis "{analysis_type}" not found in memory'}


def get_session_summary(tool_context: ToolContext):
    """
    Get a summary of all data stored in session.

    Args:
        tool_context: The ADK tool context

    Returns:
        Summary of session data
    """
    summary = {
        "student_profile": tool_context.state.get(STUDENT_PROFILE_KEY, {}),
        "analysis_count": len(tool_context.state.get(ANALYSIS_RESULTS_KEY, {})),
        "analyses_available": list(tool_context.state.get(ANALYSIS_RESULTS_KEY, {}).keys()),
        "session_timestamp": tool_context.state.get(ANALYSIS_TIMESTAMP_KEY, ""),
        "system_time": tool_context.state.get(SYSTEM_TIME_KEY, "")
    }
    
    return summary


def clear_session_data(tool_context: ToolContext):
    """
    Clear all session data except system keys.

    Args:
        tool_context: The ADK tool context

    Returns:
        A status message
    """
    keys_to_keep = [SYSTEM_TIME_KEY, RAG_INITIALIZED_KEY]
    keys_to_remove = [key for key in tool_context.state.keys() if key not in keys_to_keep]
    
    for key in keys_to_remove:
        del tool_context.state[key]
    
    return {"status": f"Cleared {len(keys_to_remove)} session data items"}


def _set_initial_state(source: Dict[str, Any], target: State | dict[str, Any]):
    """
    Set initial session state from a sample profile.

    Args:
        source: Sample profile data
        target: Session state to populate
    """
    if SYSTEM_TIME_KEY not in target:
        target[SYSTEM_TIME_KEY] = str(datetime.now())
    
    if RAG_INITIALIZED_KEY not in target:
        target[RAG_INITIALIZED_KEY] = True
        target.update(source)
        
        # Set analysis timestamp
        target[ANALYSIS_TIMESTAMP_KEY] = str(datetime.now())


def load_sample_profile(callback_context: CallbackContext):
    """
    Load a sample student profile for testing.
    Set this as a callback before_agent_call of the root_agent.

    Args:
        callback_context: The callback context
    """
    if os.path.exists(SAMPLE_PROFILE_PATH):
        try:
            with open(SAMPLE_PROFILE_PATH, "r") as file:
                data = json.load(file)
                print(f"\nLoading Sample Student Profile: {data.get('student_name', 'Unknown')}\n")
                _set_initial_state(data, callback_context.state)
        except Exception as e:
            print(f"Warning: Could not load sample profile: {e}")
    else:
        print(f"No sample profile found at {SAMPLE_PROFILE_PATH}") 