'''A tool for creating the files for a new agent.
'''
from __future__ import annotations

from default_api import write_file
from .agent_generator import generate_agent_code


def create_new_agent_files(
    agent_name: str,
    root_agent_instruction: str,
    root_agent_description: str,
    sub_agents: list[str],
) -> str:
    """Generates and writes the agent.py and __init__.py files for a new agent.

    Args:
        agent_name: The name for the new agent, which will also be used as the
            directory name (e.g., 'my_story_agent').
        root_agent_instruction: The instruction for the new root agent.
        root_agent_description: The description for the new root agent.
        sub_agents: A list of specialized agent names to include as sub_agents.

    Returns:
        A string confirming the creation of the agent files.
    """
    agent_code = generate_agent_code(
        root_agent_name=agent_name,
        root_agent_instruction=root_agent_instruction,
        root_agent_description=root_agent_description,
        sub_agents=sub_agents,
    )

    agent_py_path = f"contributing/samples/{agent_name}/agent.py"
    init_py_path = f"contributing/samples/{agent_name}/__init__.py"

    write_file(path=agent_py_path, content=agent_code)
    write_file(path=init_py_path, content="from . import agent")

    return f"Successfully created agent '{agent_name}' in contributing/samples/{agent_name}/"
