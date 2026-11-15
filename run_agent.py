import json


class RunAgent:
    """Orchestrates an agent's tool-call loop with a max_turns limit."""

    def __init__(self, agent, max_turns=5):
        self.agent = agent
        self.max_turns = max_turns

    def run(self, message):
        self.agent.messages.append({"role": "user", "content": message})

        for turn in range(self.max_turns):
            response = self.agent._call()
            msg = response.choices[0].message

            print(f"\n--- Turn {turn + 1} ---")
            print(f"finish_reason: {response.choices[0].finish_reason}")
            print(f"content:       {msg.content!r}")
            print(f"tool_calls:    {msg.tool_calls}")

            if not msg.tool_calls:
                self.agent.messages.append({"role": "assistant", "content": msg.content})
                return response

            self.agent.messages.append(msg)

            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                tool = self.agent.tool_map[name]
                result = tool.calculate(**args)

                print(f"  -> {name}({args}) = {result}")

                self.agent.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                })

        print(f"\n--- Max turns ({self.max_turns}) reached ---")
        self.agent.messages.append({"role": "assistant", "content": msg.content})
        return response
