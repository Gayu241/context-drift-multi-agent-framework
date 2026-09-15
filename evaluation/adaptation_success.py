"""
adaptation_success.py

Adaptation Success Rate (ASR)

Measures the proportion of recoverable belief error
that was corrected by the adaptation mechanism.

ASR = (BRA_after - BRA_before) /
      (1 - BRA_before)

Interpretation:

0.0
    No recovery.

0.0 < ASR < 1.0
    Partial recovery.

1.0
    Complete recovery to the expected belief.

Negative values
    Adaptation made the belief worse.
    These are clipped to 0 for the success-rate metric.

Values are bounded to [0, 1].
"""

from evaluation.metrics import EvaluationMetric


class AdaptationSuccessRate(EvaluationMetric):

    def __init__(self):

        super().__init__(
            "Adaptation Success Rate"
        )

    # =====================================================
    # EVALUATE
    # =====================================================

    def evaluate(
        self,
        bra_before,
        bra_after
    ) -> float:

        # -------------------------------------------------
        # Clamp inputs to valid BRA range
        # -------------------------------------------------

        bra_before = max(
            0.0,
            min(1.0, float(bra_before))
        )

        bra_after = max(
            0.0,
            min(1.0, float(bra_after))
        )

        # -------------------------------------------------
        # No recoverable error exists
        # -------------------------------------------------

        if bra_before >= 1.0:

            return 1.0 if bra_after >= 1.0 else 0.0

        # -------------------------------------------------
        # Calculate recoverable improvement
        # -------------------------------------------------

        recoverable_error = (
            1.0 - bra_before
        )

        improvement = (
            bra_after - bra_before
        )

        asr = (
            improvement
            / recoverable_error
        )

        # -------------------------------------------------
        # Bound to [0, 1]
        # -------------------------------------------------

        return max(
            0.0,
            min(1.0, asr)
        )

    # =====================================================
    # IMPROVEMENT
    # =====================================================

    def improvement(
        self,
        bra_before,
        bra_after
    ):

        return (
            float(bra_after)
            - float(bra_before)
        )