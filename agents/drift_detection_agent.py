"""
drift_detection_agent.py

Consumes ContextChange events and estimates the amount of
conversational context drift.
"""

from typing import List

from core.context_change import ContextChange
from core.drift_report import DriftReport


class DriftDetectionAgent:
    """
    Computes conversational drift from ContextChange events.
    """

    def __init__(self):

        # Previous drift score (Dt-1)
        self.previous_drift = 0.0

        # Equilibrium parameters
        self.alpha = 0.7
        self.beta = 0.3

    def detect(
        self,
        changes: List[ContextChange],
        total_slots: int
    ) -> DriftReport:

        if not changes:

            return DriftReport(
                turn_id=-1,
                drift_score=0.0,
                weighted_drift_score=0.0,
                equilibrium_score=0.0,
                drift_level="NO_DRIFT",
                context_changes=[]
            )

          

        turn_id = changes[0].turn_id

        drift_score = self._compute_raw_drift(
            changes,
            total_slots
        )

        weighted = self._compute_weighted_drift(
            changes,
            total_slots
        )

        equilibrium = (
            self.alpha * weighted
            + self.beta * (weighted - self.previous_drift)
        )

        self.previous_drift = weighted

        level = self._classify_drift(weighted)

        return DriftReport(
            turn_id=turn_id,
            drift_score=drift_score,
            weighted_drift_score=weighted,
            equilibrium_score=equilibrium,
            drift_level=level,
            context_changes=changes
        )

    # --------------------------------------------------

    def _compute_raw_drift(
        self,
        changes: List[ContextChange],
        total_slots: int
    ) -> float:

        if total_slots == 0:
            return 0.0

        return len(changes) / total_slots

    # --------------------------------------------------

    def _compute_weighted_drift(
        self,
        changes: List[ContextChange],
        total_slots: int
    ) -> float:

        if total_slots == 0:
            return 0.0

        total_importance = sum(
            change.importance
            for change in changes
        )

        max_importance = total_slots * 1.0

        return min(total_importance / max_importance, 1.0)

    # --------------------------------------------------

    def _classify_drift(
        self,
        score: float
    ) -> str:

        if score < 0.10:
            return "NO_DRIFT"

        if score < 0.35:
            return "LOW_DRIFT"

        if score < 0.65:
            return "MODERATE_DRIFT"

        return "HIGH_DRIFT"