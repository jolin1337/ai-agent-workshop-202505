import os
import json
import asyncio

from autogen_core.models import ModelFamily
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.tools.mcp import mcp_server_tools, StdioServerParams

# model_client = OllamaChatCompletionClient(
#    model="llama3.2:1b",
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
    name="facilitator_agent",
    model_client=model_client,
    handoffs=["user", "file_manager", "kvadrat_info_distributer"],
    system_message="""
You are a facilitator that deligates the users needs to other agents.
Deligate a task related to user information or kvadrat organization by making a handoff to kvadrat_info_distributer.
Deligate a task related to saving or preserving information by making a handoff to file_manager.
Deligate a task related to reading or listing of files by making a handoff to file_manager.
If the information needed exists in the conversation make a handoff and deligate to the user.
You can also write the word TERMINATE to close this conversation.

The handoffs should be done though calling their methods using JSON.
""",
    model_client_stream=True,  # Enable streaming tokens from the model client.
)
