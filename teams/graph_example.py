from pydantic import BaseModel, Field

import asyncio
import os
from autogen_agentchat.ui import Console
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogen_ext.models.ollama import OllamaChatCompletionClient

client = OllamaChatCompletionClient(
    model="llama3.2:3b",
    host=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434"),
    options={
        "temperature": 0.0,
    },
)
# Create an OpenAI model client
_client = OpenAIChatCompletionClient(
    model="llama3.2:3b",
    base_url=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434") + "/v1",
    api_key="sk-123",
    temperature=0.0,
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "llama",
        "structured_output": True,
    },
)


class Final(BaseModel):
    paragraph: str = Field(description="A paragraph about a specific topic")
    headline: str = Field(description="A title of the paragraph")
    topic: str = Field(description="A topic of what the paragraph is about")


# Create the writer agent
writer = AssistantAgent(
    "writer",
    model_client=client,
    system_message="Draft a short paragraph on climate change.",
)

# Create the reviewer agent
reviewer = AssistantAgent(
    "reviewer",
    model_client=client,
    system_message="Review the draft and suggest improvements. Say 'REVISE' and provide feedbacks, or 'APPROVE' for final approval.",
)
final_reviewer = AssistantAgent(
    "final_reviewer",
    model_client=client,
    system_message="Consolidate the grammar and style edits into a final version. Format it as a JSON string with the keys, topic, paragraph and headline.",
    output_content_type=Final,
)
user = UserProxyAgent(
    "user", description="A proxy for the user to approve or disapprove tasks."
)

# Build the graph
builder = (
    DiGraphBuilder()
    .add_node(final_reviewer)
    .add_node(writer)
    .add_node(reviewer)
    .add_edge(writer, reviewer)
    .add_edge(reviewer, writer, condition="REVISE")
    .add_edge(reviewer, final_reviewer, condition="APPROVE")
    .set_entry_point(writer)
)

# Build and validate the graph
graph = builder.build()

# Create the flow
flow = GraphFlow(builder.get_participants(), graph=graph)


async def main():
    stream = flow.run_stream(task="Write a short paragraph about climate change.")
    await Console(stream)


if __name__ == "__main__":
    asyncio.run(main())
