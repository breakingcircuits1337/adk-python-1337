'''Tools for managing and inspecting agents within the project.
'''
from __future__ import annotations

from default_api import run_terminal_command, read_file, write_file
from .agent_generator import generate_agent_code


def list_agents() -> str:
    """Lists all the agent directories within the 'contributing/samples' directory."""
    # Using ls -F to easily distinguish directories (they end with '/')
    result = run_terminal_command(command="ls -F contributing/samples/")
    if result["run_terminal_command_response"]["status"] == "succeeded":
        output = result["run_terminal_command_response"]["result"]
        # Filter for directories and clean up the names
        directories = [line.replace('/', '') for line in output.split('\n') if line.endswith('/')]
        return f"Successfully listed agents: {directories}"
    else:
        return f"Error listing agents: {result['run_terminal_command_response']['error']}"


def read_agent_code(agent_name: str) -> str:
    """Reads the content of the agent.py file for a specified agent."""
    path = f"contributing/samples/{agent_name}/agent.py"
    response = read_file(path=path)
    if response["read_file_response"]["status"] == "succeeded":
        return response["read_file_response"]["result"]
    else:
        return f"Error reading agent code for '{agent_name}'. Does it exist?"


def delete_agent(agent_name: str) -> str:
    """Deletes the entire directory for a specified agent."""
    path = f"contributing/samples/{agent_name}"
    # Using rm -rf for recursive, forced deletion to ensure the directory is gone.
    result = run_terminal_command(command=f"rm -rf {path}")
    if result["run_terminal_command_response"]["status"] == "succeeded":
        return f"Successfully deleted agent '{agent_name}'."
    else:
        return f"Error deleting agent '{agent_name}': {result['run_terminal_command_response']['error']}"

def update_agent_code(
    agent_name: str,
    new_instruction: str,
    new_description: str,
    new_sub_agents: list[str],
) -> str:
    """Updates an existing agent's agent.py file with new parameters.

    This will completely overwrite the existing agent.py file.
    The calling agent is responsible for providing all parameters (instruction,
    description, sub_agents), even those that are not being changed.
    Use `read_agent_code` to get the current values first if needed.

    Args:
        agent_name: The name of the agent to update (e.g., 'my_story_agent').
        new_instruction: The new instruction for the root agent.
        new_description: The new description for the root agent.
        new_sub_agents: The complete list of sub_agent names for the agent.

    Returns:
        A string confirming the update.
    """
    agent_code = generate_agent_code(
        root_agent_name=agent_name,
        root_agent_instruction=new_instruction,
        root_agent_description=new_description,
        sub_agents=new_sub_agents,
    )

    agent_py_path = f"contributing/samples/{agent_name}/agent.py"

    write_file(path=agent_py_path, content=agent_code)

    return f"Successfully updated agent code for '{agent_name}'."