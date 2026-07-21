# Ohio Legal Compliance PoE

Lightweight repository for a Proof-of-Execution (PoE) workflow that checks Ohio contract clauses for compliance with Ohio statutes and generates recommendations.

Contents:
- `agents/` — agent implementations used by the workflow
- `workflows/` — orchestration logic for the PoE workflow
- `tools/` — helper tools for statute lookups
- `models/` — simple data models such as `ComplianceReport`

Quick start:

1. Install dependencies: `pip install -r requirements.txt`
2. Run the demo runner: `python app.py`
