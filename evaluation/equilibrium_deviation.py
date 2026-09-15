"""
equilibrium_deviation.py

Implements the Equilibrium Deviation Score (EDS)
proposed in this research.
"""

from evaluation.metrics import EvaluationMetric


class EquilibriumDeviationScore(EvaluationMetric):

    def __init__(self,
                 alpha=0.7,
                 beta=0.3):

        super().__init__("Equilibrium Deviation Score")

        self.alpha = alpha
        self.beta = beta

    def evaluate(
        self,
        current_drift,
        previous_drift
    ):

        return (

            self.alpha * current_drift +

            self.beta * (current_drift - previous_drift)

        )