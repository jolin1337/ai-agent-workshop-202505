import os
from autogen_core.models import ModelFamily
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

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
system_message = """
Utifrån frågan, vilka agenter skulle du behöva fråga för att få ett svar på den?
Agenterna som är tillgängliga:
    kvadrat_info_distributer: Använder verktyg som kan hitta information inom kvadrat.
    file_manager: hanterar filer och lagrar viktig information för framtida hantering

Svara enbart med den agenten som kan svara på frågan.
"""
agent = AssistantAgent(
    "PlanningAgent",
    description="An agent for planning tasks, this agent should be the first to engage when given a new task.",
    model_client=model_client,
    system_message=system_message,
)
