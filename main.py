import os
from openai import OpenAI
from agent_response import AgentResponse
from tools import CalculatorTool
from run_agent import RunAgent

def load_env(path=".env"):
    """Read KEY=VALUE lines from a .env file into os.environ. I dont want to import dotenv just for this."""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ.setdefault(key, value)
    except FileNotFoundError:
        pass 

load_env()

class Agent:
    """A simple AI agent that can answer questions (via OpenRouter)"""

    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        self.model = "anthropic/claude-sonnet-4.6"
        #self.model = "ling-3.2-flash:free"
        self.system_message = "You are a helpful assistant that breaks down problems into steps and solves them systematically."
        
    def chat(self, message):
        """Process a user message and return a response"""

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": message},
            ],
            extra_body={"reasoning": {"enabled": True}},
            temperature=0.1,
        )

        return response

class Agent_short_memory(Agent):
    """A simple AI agent that can answer questions (via OpenRouter) with short-term memory of previous messages in the conversation"""

    def __init__(self):
        super().__init__()
        self.messages = []

    def chat(self, message):
        """Process a user message and return a response with a short-term memory"""

        self.messages.append({"role": "user", "content": message})

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "system", "content": self.system_message}] + self.messages,
            extra_body={"reasoning": {"enabled": True}},
            temperature=0.1,
        )

        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})

        return response

class Agent_short_memory_tools(Agent_short_memory):
    """A simple AI agent that can answer questions (via OpenRouter) with short-term memory of previous messages in the conversation that have access to tools"""

    def __init__(self, tools=None):
        super().__init__()
        self.tools = tools or []
        self.tool_map = {tool.get_schema()["function"]["name"]: tool for tool in self.tools}

    def _get_tool_schemas(self):
        return [tool.get_schema() for tool in self.tools]

    def _call(self):
        """Make a single API call using the current message history."""
        return self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "system", "content": self.system_message}] + self.messages,
            tools=self._get_tool_schemas() if self.tools else None,
            extra_body={"reasoning": {"enabled": True}},
            temperature=0.1
        )

    def chat(self, message):
        """Process a user message and return a response with a short-term memory"""

        self.messages.append({"role": "user", "content": message})
        response = self._call()
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})

        return response
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run an AI agent via OpenRouter")
    parser.add_argument(
        "--agent",
        choices=["basic", "memory", "tools"],
        default="basic",
        help="Which agent to use (default: basic)",
    )
    args = parser.parse_args()

    questions = [
        "I have 4 apples. How many do you have?",
        "I ate 1 apple. How many are left?",
        "What is 157.09 * 493.89?"
    ]

    if args.agent == "basic":
        agent = Agent()
        for question in questions:
            response = AgentResponse.from_completion(question, agent.chat(question))
            print(response)

    elif args.agent == "memory":
        agent = Agent_short_memory()
        for question in questions:
            response = AgentResponse.from_completion(question, agent.chat(question))
            print(response)

    elif args.agent == "tools":
        calculator = CalculatorTool()
        agent = Agent_short_memory_tools(tools=[calculator])
        runner = RunAgent(agent, max_turns=5)
        for question in questions:
            raw = runner.run(question)
            for field, value in raw:
                print((field, value))
    