from dataclasses import dataclass, asdict

__version__ = "0.1.0"


@dataclass
class ComplianceReport:
    clause: str
    state: str

    statutes: str = ""

    compliance_status: str = ""

    justification: str = ""

    recommendations: str = ""

    def to_dict(self):
        """Return a plain dict representation of the report."""
        return asdict(self)