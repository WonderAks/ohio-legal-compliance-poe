from workflows.poe_workflow import OhioComplianceWorkflow

# Module version
__version__ = "0.1.0"

def get_version():
    """Return the current application version."""
    return __version__


# Create the PoE Workflow
workflow = OhioComplianceWorkflow(
    name="Ohio Contract Compliance PoE"
)

# User Input
clause = input("Enter Contract Clause:\n\n")

# Run Workflow
result = workflow.run(
    clause=clause,
    state="Ohio",
)

# Final Report
print("\n" + "=" * 70)
print("              OHIO CONTRACT COMPLIANCE REPORT")
print("=" * 70)

print("\nState: Ohio")

print("\nContract Clause:")
print(clause)

print("\n" + "-" * 70)
print("RELEVANT STATUTES")
print("-" * 70)
print(result["statutes"])

print("\n" + "-" * 70)
print("COMPLIANCE ANALYSIS")
print("-" * 70)
print(result["compliance"])

print("\n" + "-" * 70)
print("RECOMMENDATIONS")
print("-" * 70)
print(result["recommendation"])

print("\n" + "=" * 70)
print("                 END OF REPORT")
print("=" * 70)