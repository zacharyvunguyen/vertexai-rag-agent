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

import pathlib

from google.adk.evaluation.agent_evaluator import AgentEvaluator

import dotenv
import pytest


@pytest.fixture(scope='session', autouse=True)
def load_env():
    dotenv.load_dotenv()


def test_eval_full_conversation():
    """Test the agent's basic ability on a few examples."""
    AgentEvaluator.evaluate(
       agent_module="rag",
       eval_dataset_file_path_or_dir=str(pathlib.Path(__file__).parent / "data/conversation.test.json"),
       num_runs=1,
    )