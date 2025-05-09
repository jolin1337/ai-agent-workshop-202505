import os
import json
import asyncio

from autogen_core.models import ModelFamily
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import Handoff
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import mcp_server_tools, StdioServerParams

from autogen_ext.models.ollama import OllamaChatCompletionClient


config = (
    json.load(open("tools/mcp_config.json", "r"))
    .get("mcpServers", {})
    .get("kvadrat_intern")
)
envs = dict(
    var.split("=", 1)
    for var in open(".env", "r").read().split("\n")
    if "=" in var and not var.strip().startswith("#")
)
tools = asyncio.run(mcp_server_tools(StdioServerParams(**config, env=envs)))
# model_client = OllamaChatCompletionClient(
#    model="llama3.2:3b",
#    host=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434"),
#    options={
#        "temperature": 0.0,
#    },
# )
model_client = OpenAIChatCompletionClient(
    model="llama3.2:3b",
    base_url=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434") + "/v1",
    api_key="sk-123",
    temperature=0.0,
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.ANY,
        "structured_output": True,
    },
)


agent = AssistantAgent(
    name="kvadrat_info_distributer",
    model_client=model_client,
    tools=tools,
    # handoffs=[
    #    Handoff(
    #        name="facilitator_agent",
    #        target="facilitator_agent",
    #        description="This agent can facilitate among a lot of agents to answer the question a lot better than you can",
    #    )
    # ],
    system_message="""
Du har verktygen som kan presentera nyheter och annan information från kvadrat.
Du kan exempelvis visa användarens information, nyheter och uppdrag.

Verktygen svarar med JSON men din uppgift är extrahera den efterfrågade informationen i ett läsbart format.
""",
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enable streaming tokens from the model client.
)


async def main():
    await Console(
        agent.run_stream(task="Vem är jag och vad har jag för telefonnummer?")
    )
    await agent.on_reset(None)
    await Console(agent.run_stream(task="Vilka nyheter har jag idag?"))
    await agent.on_reset(None)
    await Console(agent.run_stream(task="Vad har jag för händelser?"))
    await agent.on_reset(None)
    await Console(agent.run_stream(task="Vad har jag för uppdrag?"))


if __name__ == "__main__":
    asyncio.run(main())
