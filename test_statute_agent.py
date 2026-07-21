from agents.statute_agent import statute_agent

response = statute_agent.run(
    """
State: Ohio

Clause:

The agreement for the sale of goods worth $1000 was made orally.
"""
)

print(response.content)