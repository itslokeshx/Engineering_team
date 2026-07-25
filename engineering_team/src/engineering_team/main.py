#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
import os

import engineering_team.patch  # noqa: F401 — applies CrewAI MCP monkey-patch on import
from engineering_team.crew import EngineeringTeam
from .tools.sandbox_tools import reset_sandbox

import litellm
litellm.num_retries = 10

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


requirements = """
A simple command-line-style todo list manager, exposed via a backend class and a Gradio UI.

The system should allow users to:
- Add a task with a title and a priority level (low, medium, high).
- Mark a task as complete by its task ID.
- Remove a task by its task ID.
- List all tasks, optionally filtered by status (pending or completed).
- List all tasks, optionally filtered by priority.
- Get a count of pending vs completed tasks.

Each task should have: an auto-incrementing integer ID, title, priority, and completed status (boolean).
The system should raise a clear error if someone tries to complete or remove a task ID that doesn't exist.
No persistence to disk is required — an in-memory list is fine for this version.
"""


def run():
    """
    Run the crew.
    """
    inputs = {
        'requirements': requirements,
    }

    try:
        reset_sandbox()
        EngineeringTeam().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        EngineeringTeam().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        EngineeringTeam().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = EngineeringTeam().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
