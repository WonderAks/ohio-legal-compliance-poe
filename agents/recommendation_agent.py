__version__ = "0.1.0"

from agno.agent import Agent
from agno.models.ollama import Ollama

recommendation_agent = Agent(
    name="Recommendation Expert",
    model=Ollama(id="qwen2.5:7b"),
    description="Provides recommendations to improve compliance.",
instructions="""
You are an Ohio Legal Drafting Expert.

You will receive:

- Contract Clause
- Compliance Status
- Justification

Return EXACTLY in this format.

Recommendations:

- Recommendation 1
- Recommendation 2
- Recommendation 3

If the contract is already compliant, return:

Recommendations:
None.
""",
    markdown=True,
)