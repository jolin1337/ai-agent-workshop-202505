

import marimo

__generated_with = "0.13.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Links
        * Tools in OpenWebUI: [./openwebui/open_webui_intranet.py]()
        * Ingest for RAG with crawl4ai: https://docs.crawl4ai.com/core/deep-crawling/
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Queries
        * RoundRobin Verify - What is the composition, symbol and atomic number of helium?
        """
    )
    return


@app.cell
def _():
    ### RoundRobin Verify
    return


@app.cell
def _(false, true):
    ### RoundRobin Verify
    {
      "provider": "autogen_agentchat.teams.RoundRobinGroupChat",
      "component_type": "team",
      "version": 1,
      "component_version": 1,
      "description": "A single AssistantAgent (with a calculator tool) in a RoundRobinGroupChat team. ",
      "label": "RoundRobin Verify each answer Team",
      "config": {
        "participants": [
          {
            "provider": "autogen_agentchat.agents.AssistantAgent",
            "component_type": "agent",
            "version": 1,
            "component_version": 1,
            "description": "An agent that provides assistance with tool use.",
            "label": "AssistantAgent",
            "config": {
              "name": "assistant_agent",
              "model_client": {
                "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
                "component_type": "model",
                "version": 1,
                "component_version": 1,
                "description": "Chat completion client for OpenAI hosted models.",
                "label": "QwenOllamaChatCompletionClient",
                "config": {
                  "model": "qwen2.5-coder:7b",
                  "base_url": "http://10.68.0.247:11434/v1",
                  "api_key": "sk-123",
                  "model_info": {
                    "vision": false,
                    "function_calling": true,
                    "json_output": true,
                    "family": "llama",
                    "structured_output": true
                  },
                  "temperature": 0
                }
              },
              "tools": [
                {
                  "provider": "autogen_core.tools.FunctionTool",
                  "component_type": "tool",
                  "version": 1,
                  "component_version": 1,
                  "description": "Create custom tools by wrapping standard Python functions.",
                  "label": "FunctionTool",
                  "config": {
                    "source_code": "def calculator(a: float, b: float, operator: str) -> str:\n    try:\n        if operator == \"+\":\n            return str(a + b)\n        elif operator == \"-\":\n            return str(a - b)\n        elif operator == \"*\":\n            return str(a * b)\n        elif operator == \"/\":\n            if b == 0:\n                return \"Error: Division by zero\"\n            return str(a / b)\n        else:\n            return \"Error: Invalid operator. Please use +, -, *, or /\"\n    except Exception as e:\n        return f\"Error: {str(e)}\"\n",
                    "name": "calculator",
                    "description": "A simple calculator that performs basic arithmetic operations",
                    "global_imports": [],
                    "has_cancellation_support": false
                  }
                },
                {
                  "provider": "autogen_core.tools.FunctionTool",
                  "component_type": "tool",
                  "version": 1,
                  "component_version": 1,
                  "description": "A tool that lookups and returns explanations of known terms and single words.",
                  "label": "Search DuckDukcGo",
                  "config": {
                    "source_code": "def extract_terms_ddg( query: str) -> dict:\n    url = \"https://www.searchapi.io/api/v1/search\"\n    params = {\n        \"q\": query,\n        \"format\": \"json\",\n        \"redirected\": \"1\",\n    }\n\n    response = requests.get(f'https://api.duckduckgo.com', params=params)\n    return response.json()",
                    "name": "extract_terms_ddg",
                    "description": "A simple calculator that performs basic arithmetic operations",
                    "global_imports": [
                      "requests"
                    ],
                    "has_cancellation_support": false
                  }
                }
              ],
              "model_context": {
                "provider": "autogen_core.model_context.UnboundedChatCompletionContext",
                "component_type": "chat_completion_context",
                "version": 1,
                "component_version": 1,
                "description": "An unbounded chat completion context that keeps a view of the all the messages.",
                "label": "UnboundedChatCompletionContext",
                "config": {}
              },
              "description": "An agent that provides assistance with ability to use tools.",
              "system_message": "Answer the question of the user as straight as possible. You have the following tools that you could call if necessary:\n* Use extract_terms_ddg tool with one word per query if you need more information about it.\n* Use calculator tool if the user asks about simple arethemtics.",
              "model_client_stream": false,
              "reflect_on_tool_use": true,
              "tool_call_summary_format": "{result}"
            }
          },
          {
            "provider": "autogen_agentchat.agents.AssistantAgent",
            "component_type": "agent",
            "version": 1,
            "component_version": 1,
            "description": "an agent that verifies and summarizes information",
            "label": "Verification Assistant",
            "config": {
              "name": "VerificationAssistant",
              "model_client": {
                "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
                "component_type": "model",
                "version": 1,
                "component_version": 1,
                "description": "Chat completion client for OpenAI hosted models.",
                "label": "OllamaChatCompletionClient",
                "config": {
                  "model": "llama3.2:3b",
                  "base_url": "http://10.68.0.247:11434/v1",
                  "api_key": "sk-123",
                  "model_info": {
                    "vision": false,
                    "function_calling": true,
                    "json_output": true,
                    "family": "llama",
                    "structured_output": true
                  },
                  "temperature": 0
                }
              },
              "tools": [],
              "model_context": {
                "provider": "autogen_core.model_context.UnboundedChatCompletionContext",
                "component_type": "chat_completion_context",
                "version": 1,
                "component_version": 1,
                "description": "An unbounded chat completion context that keeps a view of the all the messages.",
                "label": "UnboundedChatCompletionContext",
                "config": {}
              },
              "description": "an agent that verifies and summarizes information",
              "system_message": "Does it answer the original question the user had? If so respond with TERMINATE, else explain what more needs to be added.",
              "model_client_stream": false,
              "reflect_on_tool_use": false,
              "tool_call_summary_format": "{result}"
            }
          }
        ],
        "termination_condition": {
          "provider": "autogen_agentchat.base.OrTerminationCondition",
          "component_type": "termination",
          "version": 1,
          "component_version": 1,
          "label": "OrTerminationCondition",
          "config": {
            "conditions": [
              {
                "provider": "autogen_agentchat.conditions.TextMentionTermination",
                "component_type": "termination",
                "version": 1,
                "component_version": 1,
                "description": "Terminate the conversation if a specific text is mentioned.",
                "label": "TextMentionTermination",
                "config": {
                  "text": "TERMINATE"
                }
              },
              {
                "provider": "autogen_agentchat.conditions.MaxMessageTermination",
                "component_type": "termination",
                "version": 1,
                "component_version": 1,
                "description": "Terminate the conversation after a maximum number of messages have been exchanged.",
                "label": "MaxMessageTermination",
                "config": {
                  "max_messages": 10,
                  "include_agent_event": false
                }
              }
            ]
          }
        }
      }
    }
    return


@app.cell
def _(mo):
    mo.md(r"""### RAG Graph""")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
