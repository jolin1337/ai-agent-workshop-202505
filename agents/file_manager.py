import os
import json
import asyncio

from autogen_core.models import ModelFamily
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.tools.mcp import mcp_server_tools, StdioServerParams


config = (
    json.load(open("tools/mcp_config.json", "r"))
    .get("mcpServers", {})
    .get("filesystem")
)
tools = asyncio.run(mcp_server_tools(StdioServerParams(**config)))
model_client = OpenAIChatCompletionClient(
    model="llama3.2:1b",
    base_url=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434") + "/v1",
    api_key="sk-123",
    temperature=0.0,
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.ANY,
        "structured_output": False,
    },
)
model_client = OllamaChatCompletionClient(
    model="llama3.2:1b",
    host=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434"),
    options={
        "temperature": 0.0,
    },
)


agent = AssistantAgent(
    name="file_manager",
    model_client=model_client,
    tools=tools,
    system_message="Logga informationen i chat historiken genom att anropa write_file i filen 2025-05-04.",
    # handoffs=["facilitator"],
    #    system_message="""
    # Du agerar som ett anteckningsstöd och lagrar dina anteckningar i filer.
    # Lagra all relevant information som givits i filer med relevanta namn.
    # Är ett namn explicit skrivet använd detta.
    # Berätta för användaren när du har anropat någon av verktygen och berätta status vad som returnerades.
    # """,
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enable streaming tokens from the model client.
)


async def main():
    await Console(
        agent.run_stream(task="I want you to remember that I like the color green")
    )
    await Console(
        agent.run_stream(
            task='Save a file named hello_world.txt with content "foo=bar"'
        )
    )
    await Console(
        agent.run_stream(
            task="Tell me the contents in the file with name hello_world.txt"
        )
    )
    await Console(agent.run_stream(task="what files exists in the root folder?"))
    await Console(agent.run_stream(task="Delete the file named hello_world.txt"))
    await Console(agent.run_stream(task="what files exists in the root folder?"))
    await Console(
        agent.run_stream(
            task='Save a file named hello_world.txt with content "foo=bar"'
        )
    )
    await Console(
        agent.run_stream(task="Delete all the files you can find to clear everything")
    )


if __name__ == "__main__":
    asyncio.run(main())
