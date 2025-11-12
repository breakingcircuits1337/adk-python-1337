'''A tool for running and testing an agent.
'''
from __future__ import annotations

from default_api import run_terminal_command


def run_agent(agent_name: str) -> str:
    """Runs the specified agent in an interactive CLI session.

    This will start the 'adk run' command, allowing the user to interact with
    the agent directly from their terminal.

    Args:
        agent_name: The name of the agent to run.

    Returns:
        A confirmation message that the agent is being started.
    """
    path = f"contributing/samples/{agent_name}"
    # This command will take over the user's terminal for an interactive session.
    # The tool doesn't return the result of the session, just confirms it started.
    result = run_terminal_command(command=f"adk run {path}")

    # We might not get a clean success/fail here if the command launches
    # an interactive process. We will assume it works if the command is sent.
    if result["run_terminal_command_response"]["status"] == "succeeded":
        return f"Starting interactive session for agent '{agent_name}'. Check your terminal to interact with it."
    else:
        return f"Error attempting to run agent '{agent_name}': {result['run_terminal_command_response']['error']}"
