import json

from tools.ohio_statute_tool import OhioStatuteTool
from agents.statute_agent import statute_agent
from agents.compliance_agent import compliance_agent


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
    if case["id"] == 12
)


clause = test["clause"]


print("=" * 70)
print("TEST CASE 12 - FULL COMPLIANCE PIPELINE DEBUG")
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

statute_response = statute_agent.run(
    f"""
Contract Clause:

{clause}

Candidate Ohio Statutes:

{tool_output}

Identify all directly relevant Ohio statute sections
from the candidate statutes provided.
"""
)

statute_output = statute_response.content

print(statute_output)


print("\n\nCOMPLIANCE AGENT OUTPUT")
print("-" * 70)

compliance_response = compliance_agent.run(
    f"""
Contract Clause:

{clause}

Relevant Ohio Statutes:

{statute_output}

Retrieved Ohio Statute Evidence:

{tool_output}

Determine the compliance status of the contract clause
using only the Ohio statute evidence provided.
"""
)

print(compliance_response.content)


print("\n\nEXPECTED GROUND TRUTH")
print("-" * 70)

print(
    "Expected Statutes:",
    test["expected_statutes"]
)

print(
    "Expected Compliance:",
    test["expected_compliance"]
)


print("\n" + "=" * 70)
print("END DEBUG")
print("=" * 70)