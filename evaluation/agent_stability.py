"""
agent_stability.py

Agent Stability Index (ASI)

Measures how stable the framework remains across
the entire conversation.
"""

import statistics

from evaluation.metrics import EvaluationMetric


class AgentStabilityIndex(EvaluationMetric):

    def __init__(self):

        super().__init__("Agent Stability Index")

    # ---------------------------------------------------------

    def evaluate(

        self,

        drift_reports

    ) -> float:

        if len(drift_reports) <= 1:

            return 1.0

        scores = [

            report.weighted_drift_score

            for report in drift_reports

        ]

        std = statistics.pstdev(scores)

        stability = 1.0 - std

        return max(0.0, stability)

    # ---------------------------------------------------------

    def drift_profile(

        self,

        drift_reports

    ):

        return [

            report.weighted_drift_score

            for report in drift_reports

        ]