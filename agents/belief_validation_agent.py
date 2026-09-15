"""
belief_validation_agent.py

Validates whether a belief state is internally consistent.
"""

from core.belief_state import BeliefState
from core.validation_report import ValidationReport


class BeliefValidationAgent:

    """
    Performs rule-based validation of belief states.
    """

    def validate(self, belief_state: BeliefState) -> ValidationReport:

        issues = []
        validated = []

        for slot, value in belief_state.slots.items():

            # Skip empty values
            if value in ("", None, "not mentioned"):
                continue

            validated.append(slot)

            # Numeric validation
            if slot in ["people", "stay"]:

                try:
                    if int(value) <= 0:
                        issues.append(
                            f"{slot} must be greater than zero."
                        )

                except ValueError:
                    issues.append(
                        f"{slot} should contain a numeric value."
                    )

        return ValidationReport(
            turn_id=belief_state.turn_id,
            is_valid=len(issues) == 0,
            confidence=belief_state.confidence,
            issues=issues,
            validated_slots=validated
        )