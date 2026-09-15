"""
equilibrium_recovery.py

Measures how effectively equilibrium deviation
is reduced after adaptation.

ERR measures the proportion of the pre-adaptation
equilibrium deviation that was recovered.

ERR = (|E_before| - |E_after|) / |E_before|

ERR is bounded to [0, 1].
"""

from evaluation.metrics import EvaluationMetric


class EquilibriumRecoveryRate(EvaluationMetric):

    def __init__(self):

        super().__init__(
            "Equilibrium Recovery Rate"
        )

    # =====================================================
    # EVALUATE
    # =====================================================

    def evaluate(
        self,
        equilibrium_before,
        equilibrium_after
    ):

        before = abs(
            float(equilibrium_before)
        )

        after = abs(
            float(equilibrium_after)
        )

        # -------------------------------------------------
        # No equilibrium deviation existed.
        # -------------------------------------------------

        if before == 0.0:

            return (
                1.0
                if after == 0.0
                else 0.0
            )

        # -------------------------------------------------
        # Fraction of deviation recovered.
        # -------------------------------------------------

        recovery = (
            before - after
        ) / before

        # -------------------------------------------------
        # Bound to [0, 1].
        # -------------------------------------------------

        return max(
            0.0,
            min(
                1.0,
                recovery
            )
        )