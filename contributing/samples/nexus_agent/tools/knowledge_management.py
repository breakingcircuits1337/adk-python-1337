'''A tool for managing the Nexus Agent Builder's knowledge of specialized agent types.
'''
from __future__ import annotations

from default_api import read_file, write_file


def add_new_agent_type(
    name: str,
    instruction: str,
    description: str,
    has_google_search: bool = False,
) -> str:
    """Adds a new specialized agent definition to the builder's knowledge base.

    This allows the Nexus Agent Builder to create new types of agents that are
    not in its initial set.

    Args:
        name: The name for the new agent type (e.g., 'story_writer_agent').
        instruction: The instruction for this new type of agent.
        description: The description for this new type of agent.
        has_google_search: Whether this agent type should have the google_search
            tool. Defaults to False.

    Returns:
        A string confirming that the new agent type was added.
    """
    generator_path = "contributing/samples/nexus_agent/tools/agent_generator.py"

    # Read the existing generator code
    read_response = read_file(path=generator_path)
    if read_response["read_file_response"]["status"] != "succeeded":
        return f"Error: Could not read the agent_generator.py file."
    
    content = read_response["read_file_response"]["result"]

    # Construct the new agent definition block
    tools_list = "[google_search]" if has_google_search else "[]"
    new_definition = f"""    "{name}": '''
{name} = Agent(
    name="{name}",
    model="gemini-1.5-flash",
    instruction="""{instruction}""",
    description="""{description}""",
    tools={tools_list},
)
''',"""

    # Find the insertion point in the AGENT_DEFINITIONS dictionary
    # We'll insert it right before the end of the dictionary
    insertion_marker = "}\n\ndef generate_agent_code("
    if insertion_marker not in content:
        return "Error: Could not find the insertion point in agent_generator.py."

    parts = content.split(insertion_marker)
    new_content = parts[0] + new_definition + "\n" + insertion_marker + parts[1]

    # Write the modified content back to the file
    write_response = write_file(path=generator_path, content=new_content)
    if write_response["write_file_response"]["status"] == "succeeded":
        return f"Successfully added the new specialized agent type: '{name}'."
    else:
        return "Error: Could not write the updated content to agent_generator.py."
