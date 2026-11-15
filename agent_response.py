from dataclasses import dataclass

@dataclass
class AgentResponse:
    """The parts of a model reply that we care about."""
    question: str
    answer: str
    reasoning: str | None = None

    @classmethod
    def from_completion(cls, question, completion):
        """Build an AgentResponse from an OpenAI/OpenRouter ChatCompletion."""
        msg = completion.choices[0].message
        return cls(
            question=question,
            answer=msg.content or "",
            reasoning=getattr(msg, "reasoning", None),
        )

    def __str__(self):
        return (
            f"[?] Question: {self.question}\n"
            f"[i] Reasoning: {self.reasoning}\n"
            f"[>] Answer: {self.answer}\n"
        )