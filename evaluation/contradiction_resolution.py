"""
contradiction_resolution.py

Contradiction Resolution Rate (CRR)

Measures the percentage of contradictory beliefs
that were successfully repaired.
"""

from evaluation.metrics import EvaluationMetric


class ContradictionResolutionRate(EvaluationMetric):

    def __init__(self):

        super().__init__("Contradiction Resolution Rate")

    def evaluate(
        self,
        contradictions_found: int,
        contradictions_resolved: int
    ) -> float:

        if contradictions_found == 0:
            return 1.0

        return contradictions_resolved / contradictions_found