import os
import asyncio
from typing import Sequence

from autogen_core.models import ModelFamily
from autogen_agentchat.agents import (
    UserProxyAgent,
    MessageFilterAgent,
    MessageFilterConfig,
    PerSourceFilter,
)
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.conditions import (
    HandoffTermination,
    TextMentionTermination,
    MaxMessageTermination,
)
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from agents.planner import agent as planning_agent
from agents.file_manager import agent as file_manager
from agents.kvadrat_info_distributer import agent as kvadrat_info_distributer

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


def selector(messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> str | None:
    if len(messages) <= 1 or messages[-1].source == user.name:
        return planning_agent.name
    initial_plan, msg_idx = [
        (p.content, i)
        for i, p in enumerate(messages)
        if p.source == planning_agent.name
    ][-1]
    executed_agents = [p.source for p in messages[msg_idx:]]
    indicies_of_agents = [
        (initial_plan.index(p.name), p.name)
        for p in team._participants
        if p.name in initial_plan and p.name not in executed_agents
    ]
    indicies_of_agents.sort(key=lambda x: x[0])
    if indicies_of_agents:
        return indicies_of_agents[0][1]
    return None


user = UserProxyAgent(
    "user", description="A proxy for the user to approve or disapprove tasks."
)
text_mention_termination = TextMentionTermination("TERMINATE")
max_messages_termination = MaxMessageTermination(max_messages=25)
handoff_user_termination = HandoffTermination(target="user")
termination = (
    max_messages_termination | handoff_user_termination | text_mention_termination
)
selector_prompt = """
Select an agent to perform task.

{roles}

Current conversation context:
{history}

Read the above conversation, then select an agent from {participants} to perform the next task.
Make sure the facilitator agent has assigned tasks before other agents start working.
Only select one agent.
"""
participants = [planning_agent, user, file_manager, kvadrat_info_distributer]
team = SelectorGroupChat(
    [
        MessageFilterAgent(
            name=p.name,
            wrapped_agent=p,
            filter=MessageFilterConfig(
                per_source=[
                    PerSourceFilter(source="user", position="last", count=1),
                    PerSourceFilter(source=p.name, position="last", count=2),
                ]
            ),
        )
        for p in participants
    ],
    model_client=model_client,
    termination_condition=termination,
    selector_func=selector,
    allow_repeated_speaker=True,  # Allow an agent to speak multiple turns in a row.
)


task = "Vem är jag på kvadrat?"


async def run_team_stream() -> None:
    task_result = await Console(team.run_stream(task=task))
    last_message = task_result.messages[-1]
    return
    while isinstance(last_message, HandoffMessage) and last_message.target == "user":
        user_message = input("User: ")

        task_result = await Console(
            team.run_stream(
                task=HandoffMessage(
                    source="user", target=last_message.source, content=user_message
                )
            )
        )
        last_message = task_result.messages[-1]


if __name__ == "__main__":
    asyncio.run(run_team_stream())
