import json

from tools.ohio_statute_tool import OhioStatuteTool
from agents.statute_agent import statute_agent


tool = OhioStatuteTool()


with open(
    "evaluation/ohio_ground_truth.json",
    "r",
    encoding="utf-8"
) as file:
    tests = json.load(file)


test = next(
    case
    for case in tests
    if case["id"] == 11
)


clause = test["clause"]


print("=" * 70)
print("TEST CASE 11 - FULL STATUTE PIPELINE DEBUG")
print("=" * 70)


print("\nCONTRACT CLAUSE")
print("-" * 70)

print(clause)


print("\n\nRAW OHIO STATUTE TOOL OUTPUT")
print("-" * 70)

tool_output = tool.search_statutes(clause)

print(tool_output)


print("\n\nSTATUTE AGENT OUTPUT")
print("-" * 70)


response = statute_agent.run(
    f"""
Contract Clause:

{clause}

Candidate Ohio Statutes:

{tool_output}

Identify only the relevant Ohio statute sections
from the candidate statutes provided.
"""
)


print(response.content)


print("\n" + "=" * 70)
print("END DEBUG")
print("=" * 70)