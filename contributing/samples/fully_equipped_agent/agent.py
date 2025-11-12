from google.adk import Agent
from google.adk.tools import (
    google_search,
    enterprise_web_search,
    url_context,
    exit_loop,
    get_user_choice,
    load_artifacts,
    load_memory,
    preload_memory,
    transfer_to_agent,
    APIHubToolset,
    VertexAiSearchTool,
    DiscoveryEngineSearchTool,
)

root_agent = Agent(
    model="gemini-1.5-flash",
    name="fully_equipped_agent",
    description="An agent with all the pre-made tools",
    tools=[
        google_search,
        enterprise_web_search,
        url_context,
        exit_loop,
        get_user_choice,
        load_artifacts,
        load_memory,
        preload_memory,
        transfer_to_agent,
        APIHubToolset(
            openapi_spec="contributing/samples/fully_equipped_agent/openapi.yaml"
        ),
        VertexAiSearchTool(data_store_id="YOUR_DATA_STORE_ID"),
        DiscoveryEngineSearchTool(collection_id="YOUR_COLLECTION_ID"),
    ],
)
