# MCP Agent with Short-Term Memory

A minimal AI agent that demonstrates conversational short-term memory using the OpenRouter API.

## What it does

The agent maintains a message history across turns so it can reference earlier parts of the conversation. This lets it handle follow-up questions that depend on prior context -- for example, tracking how many apples you have after eating one.

Two chat modes are available:

- **Stateless** (`agent.chat()`) -- each message is independent, no memory of prior turns.
- **Short-term memory** (`agent.chat_short_memory()`) -- accumulates the conversation history and sends it with every request.

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

This runs a demo that asks two related questions and prints the reasoning and answer for each.

## Project structure

```
main.py              -- Agent class with stateless and memory-enabled chat
agent_response.py    -- AgentResponse dataclass for structured output
.env                 -- API key (not committed)
```
