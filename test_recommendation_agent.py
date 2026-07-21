from agents.recommendation_agent import recommendation_agent

response = recommendation_agent.run(
"""
Contract Clause:

The agreement for the sale of goods worth $1000 was made orally.

Compliance Status:

Non-Compliant

Justification:

Contracts above $500 must generally be in writing under Ohio Revised Code 1302.04.
"""
)

print(response.content)