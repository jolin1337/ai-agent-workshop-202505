import asyncio

from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from agents.facilitator import agent as facilitator
from agents.file_manager import agent as file_manager
from agents.kvadrat_info_distributer import agent as kvadrat_info_distributer

termination = HandoffTermination(target="user") | TextMentionTermination("TERMINATE")
team = Swarm(
    [facilitator, file_manager, kvadrat_info_distributer],
    termination_condition=termination,
    emit_team_events=False,
)


task = "Vem är jag på kvadrat?"


async def run_team_stream() -> None:
    task_result = await Console(team.run_stream(task=task))
    last_message = task_result.messages[-1]

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
