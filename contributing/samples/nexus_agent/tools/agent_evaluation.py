'''Tools for evaluating the performance of agents.
'''
from __future__ import annotations
import json

from default_api import write_file, run_terminal_command


def create_evaluation_set(
    agent_name: str,
    eval_set_name: str,
    test_cases: list[dict[str, str]],
) -> str:
    """Creates a JSON evaluation file for use with 'adk eval'.

    Args:
        agent_name: The name of the agent this eval set is for.
        eval_set_name: The name for the evaluation set file (e.g., 'initial_tests').
        test_cases: A list of dictionaries, where each dictionary contains an
            'input' (the prompt) and an 'expected_output'.

    Returns:
        A string confirming the creation of the evaluation set.
    """
    eval_data = {
        "name": f"{agent_name}-{eval_set_name}",
        "test_cases": test_cases,
    }

    file_path = f"contributing/samples/{agent_name}/{eval_set_name}.json"
    content = json.dumps(eval_data, indent=2)

    write_response = write_file(path=file_path, content=content)
    if write_response["write_file_response"]["status"] == "succeeded":
        return f"Successfully created evaluation set at: {file_path}"
    else:
        return f"Error creating evaluation set: Could not write file."


def run_evaluation(agent_name: str, eval_set_name: str) -> str:
    """Runs 'adk eval' on a specified agent and evaluation set.

    Args:
        agent_name: The name of the agent to evaluate.
        eval_set_name: The name of the evaluation set file (without .json).

    Returns:
        The output from the adk eval command.
    """
    agent_path = f"contributing/samples/{agent_name}"
    eval_path = f"contributing/samples/{agent_name}/{eval_set_name}.json"

    command = f"adk eval {agent_path} {eval_path}"
    result = run_terminal_command(command=command)

    if result["run_terminal_command_response"]["status"] == "succeeded":
        return f"Evaluation complete. Results:\n{result['run_terminal_command_response']['result']}"
    else:
        return f"Error running evaluation: {result['run_terminal_command_response']['error']}"
