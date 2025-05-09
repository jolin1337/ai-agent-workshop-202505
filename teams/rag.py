from typing import List, Literal
import json
import asyncio
import os
from autogen_agentchat.ui import Console
from pydantic import BaseModel, Field
from autogen_agentchat.agents import (
    AssistantAgent,
    UserProxyAgent,
    MessageFilterAgent,
    MessageFilterConfig,
    PerSourceFilter,
)
from autogen_agentchat.conditions import SourceMatchTermination, MaxMessageTermination
from autogen_agentchat.base import OrTerminationCondition
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.tools.mcp import mcp_server_tools, StdioServerParams

client = OllamaChatCompletionClient(
    model="llama3.2:3b",
    host=os.environ.get("OLLAMA_API_BASE", "http://localhost:11434"),
    options={
        "temperature": 0.0,
    },
)


class RelevantDocuments(BaseModel):
    relevant: List[str] = Field(description="A list of relevant documents to the query")


class HLabel(BaseModel):
    label: Literal["GROUNDED", "HALUCINATE"]
    explanation: str


class ALabel(BaseModel):
    label: Literal["ANSWERED", "UNKOWN"]
    explanation: str


config = json.load(open("tools/mcp_config.json", "r")).get("mcpServers", {}).get("rag")
tools = asyncio.run(mcp_server_tools(StdioServerParams(**config)))
# Create the writer agent
retriever = AssistantAgent(
    "retirever",
    tools=tools,
    model_client=client,
    system_message="Look in the retirever tool to find information about the question.",
    # reflect_on_tool_use=True,
)
filter = AssistantAgent(
    "filter",
    output_content_type=RelevantDocuments,
    model_client=client,
    system_message="From the documents keep only information that is relevant and write it into a JSON with key relevant_information",
)
filter = MessageFilterAgent(
    name=filter.name,
    wrapped_agent=filter,
    filter=MessageFilterConfig(
        per_source=[
            PerSourceFilter(source="user", position="last", count=1),
            PerSourceFilter(source=retriever.name, position="last", count=1),
        ]
    ),
)

rewrite_question = AssistantAgent(
    "rewrite_question",
    model_client=client,
    system_message="Reformulate the users question directed more towards what can be answered at bolagsverket",
)
rewrite_question = MessageFilterAgent(
    name=rewrite_question.name,
    wrapped_agent=rewrite_question,
    filter=MessageFilterConfig(
        per_source=[
            PerSourceFilter(source="user", position="last", count=1),
            PerSourceFilter(source=rewrite_question.name, position="last", count=20),
        ]
    ),
)
answer = AssistantAgent(
    "answer",
    model_client=client,
    system_message="Given the information answer the question grounded in the retrieved documents",
    model_client_stream=False,
)
rewrite_answer = AssistantAgent(
    "rewrite_answer",
    model_client=client,
    system_message="Reformulate the users question directed more towards what can be answered at bolagsverket",
)
rewrite_answer = MessageFilterAgent(
    name=rewrite_answer.name,
    wrapped_agent=rewrite_answer,
    filter=MessageFilterConfig(
        per_source=[
            PerSourceFilter(source="user", position="last", count=1),
            PerSourceFilter(source=answer.name, position="last", count=1),
            PerSourceFilter(source=rewrite_answer.name, position="last", count=20),
        ]
    ),
)
hallucination = AssistantAgent(
    "fact_checker",
    model_client=client,
    system_message="Make sure the answer is grounded in any of the relevant documents, if so answer 'GROUNDED', if the answer is not grounded answer 'HALUCINATE'",
    output_content_type=HLabel,
)
hallucination = MessageFilterAgent(
    name=hallucination.name,
    wrapped_agent=hallucination,
    filter=MessageFilterConfig(
        per_source=[
            PerSourceFilter(source=retriever.name, position="last", count=1),
            PerSourceFilter(source=answer.name, position="last", count=1),
        ]
    ),
)
question_answered = AssistantAgent(
    "question_checker",
    model_client=client,
    system_message="Is the given answer an answer to the question? Write 'ANSWERED' if the question is answered else 'UNKOWN' together with an explanation",
    output_content_type=ALabel,
)
question_answered = MessageFilterAgent(
    name=question_answered.name,
    wrapped_agent=question_answered,
    filter=MessageFilterConfig(
        per_source=[
            PerSourceFilter(source="user", position="last", count=1),
            PerSourceFilter(source=answer.name, position="last", count=1),
        ]
    ),
)
final_answer = AssistantAgent(
    "final_answer",
    model_client=client,
    system_message="Consolidate the grammar and style edits into a final version.",
)

# Build the graph
builder = (
    DiGraphBuilder()
    .add_node(retriever)
    .add_node(filter)
    .add_node(rewrite_question)
    .add_node(answer)
    .add_node(rewrite_answer)
    .add_node(hallucination)
    .add_node(question_answered)
    .add_node(final_answer)
    .add_edge(retriever, filter)
    .add_edge(filter, answer, '["')
    .add_edge(answer, hallucination)
    .add_edge(rewrite_question, retriever)
    # .add_edge(rewrite_answer, hallucination)
    .add_conditional_edges(
        hallucination,
        {
            "HALUCINATE": rewrite_question,
            "GROUNDED": question_answered,
        },
    )
    .add_conditional_edges(
        question_answered,
        {
            "ANSWERED": final_answer,
            "UNKOWN": rewrite_answer,
        },
    )
    # .add_edge(filter, rewrite_question, "[]")
    .set_entry_point(retriever)
)

# Build and validate the graph
graph = builder.build()

# Create the flow
flow = GraphFlow(
    builder.get_participants(),
    graph=graph,
    termination_condition=OrTerminationCondition(
        SourceMatchTermination([final_answer.name]), MaxMessageTermination(10)
    ),
)


async def main():
    mermaid = ["```mermaid", "graph TD;"]
    for node in graph.nodes.values():
        for edge in node.edges:
            condition = ""
            if edge.condition:
                condition = f"|{edge.condition}|"
            mermaid.append(
                f"   {node.name}({node.name}) --> {condition}{edge.target}({edge.target})"
            )
    mermaid.append("```")
    print("\n".join(mermaid))
    stream = flow.run_stream(task="Är äpplen röda?")
    # stream = flow.run_stream(task="Vad är en verklig huvudman?")
    result = await Console(stream)
    answer_messages = [m for m in result.messages if m.source == answer.name]
    if answer_messages:
        print("Last answer recieved:", answer_messages[-1])
    else:
        print("No answer recieved, last message:", result.messages[-1])


if __name__ == "__main__":
    asyncio.run(main())
