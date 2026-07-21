"""Workflow orchestration for the Ohio Compliance PoE.

Version: 0.1.0
"""

from agno.workflow import Workflow

from agents.statute_agent import statute_agent
from agents.compliance_agent import compliance_agent
from agents.recommendation_agent import recommendation_agent


class OhioComplianceWorkflow(Workflow):

    def run(self, clause: str, state: str = "Ohio"):

        print("\n========== STEP 1 ==========")
        print("Finding Relevant Statutes...\n")

        statutes = statute_agent.run(
            f"""
State:
{state}

Clause:
{clause}
"""
        ).content

        print(statutes)

        print("\n========== STEP 2 ==========")
        print("Checking Compliance...\n")

        compliance = compliance_agent.run(
            f"""
Contract Clause:

{clause}

Relevant Ohio Statutes:

{statutes}
"""
        ).content

        print(compliance)

        print("\n========== STEP 3 ==========")
        print("Generating Recommendations...\n")

        recommendation = recommendation_agent.run(
            f"""
Contract Clause:

{clause}

{compliance}
"""
        ).content

        print(recommendation)

        return {
            "statutes": statutes,
            "compliance": compliance,
            "recommendation": recommendation,
        }