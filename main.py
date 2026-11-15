import os
from openai import OpenAI
from agent_response import AgentResponse

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
        #self.model = "anthropic/claude-sonnet-4.6"
        self.model = "ling-3.2-flash:free"
        self.system_message = "You are a helpful assistant that breaks down problems into steps and solves them systematically."
        self.messages = [] # short-term memory
        
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

    def chat_short_memory(self, message):
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

if __name__ == "__main__":
    agent = Agent()

    questions = [
        "I have 4 apples. How many do you have?",
        "I ate 1 apple. How many are left?"
    ]

    for question in questions:
        #response = AgentResponse.from_completion(question, agent.chat(question))
        response = AgentResponse.from_completion(question, agent.chat_short_memory(question))
        print(response)