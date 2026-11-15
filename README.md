# MCP Agent with Short-Term Memory

A minimal AI agent that demonstrates conversational short-term memory and tool use via the OpenRouter API.

## What it does

The agent maintains a message history across turns so it can reference earlier parts of the conversation. This lets it handle follow-up questions that depend on prior context -- for example, tracking how many apples you have after eating one. It can also call tools (like a calculator) when the model decides it needs one.

Three agent classes are available, each building on the previous:

- **`Agent`** -- stateless, each message is independent, no memory of prior turns.
- **`Agent_short_memory`** -- accumulates conversation history and sends it with every request.
- **`Agent_short_memory_tools`** -- adds tool support (e.g. calculator). Tools are passed in at creation and their schemas are sent to the model.

`RunAgent` orchestrates the tool-call loop: it calls the agent, executes any tool calls the model requests, feeds results back, and repeats -- up to a configurable `max_turns` limit.

## Setup

1. Get an API key from [OpenRouter](https://openrouter.ai/).

2. Create a `.env` file in the project root:

   ```
   OPENROUTER_API_KEY=your-key-here
   ```

3. Install the dependency:

   ```
   pip install openai
   ```

## Usage

```
python main.py
```

This runs a demo that asks a few questions (including a math question that triggers the calculator tool) and prints the raw model response for each turn.

## Project structure

```
main.py              -- Agent classes (Agent, Agent_short_memory, Agent_short_memory_tools)
run_agent.py         -- RunAgent class that orchestrates the tool-call loop
tools.py             -- Tool definitions (CalculatorTool with get_schema())
agent_response.py    -- AgentResponse dataclass for structured output
.env                 -- API key (not committed)
```

## References

- [Build an AI Agent from Scratch in Python](https://www.leoniemonigatti.com/blog/ai-agent-from-scratch-in-python.html) -- the tutorial this project is based on
- [OpenRouter API docs](https://openrouter.ai/docs/quickstart)
- [OpenAI Python client](https://github.com/openai/openai-python) -- used here as an OpenRouter-compatible HTTP client