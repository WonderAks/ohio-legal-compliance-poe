from agents.compliance_agent import compliance_agent

response = compliance_agent.run(
"""
Contract Clause:

The agreement for the sale of goods worth $1000 was made orally.

Relevant Ohio Statutes:

Section 1302.04
Contracts for the sale of goods priced at $500 or more generally must be in writing.

Section 1335.05
Certain agreements must be in writing.
"""
)

print(response.content)