"""
validation_report.py

Represents the output of the Belief Validation Agent.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ValidationReport:
    """
    Validation result for the current conversational state.
    """

    turn_id: int

    is_valid: bool

    confidence: float

    issues: List[str] = field(default_factory=list)

    validated_slots: List[str] = field(default_factory=list)

    def __str__(self):

        return (
            f"\n"
            f"Turn: {self.turn_id}\n"
            f"Valid: {self.is_valid}\n"
            f"Confidence: {self.confidence:.2f}\n"
            f"Issues: {len(self.issues)}\n"
            f"Validated Slots: {len(self.validated_slots)}"
        )