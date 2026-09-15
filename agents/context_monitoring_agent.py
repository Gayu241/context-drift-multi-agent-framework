"""
context_monitoring_agent.py

Tracks contextual changes between consecutive belief states.

This agent does NOT determine whether drift has occurred.
Its sole responsibility is to detect and report changes.
"""

from typing import List

from core.belief_state import BeliefState
from core.context_change import ContextChange


class ContextMonitoringAgent:

    """
    Detects contextual changes between consecutive belief states.
    """

    def monitor(
        self,
        previous: BeliefState,
        current: BeliefState
    ) -> List[ContextChange]:

        changes = []
        # Skip completely empty belief states

        if not previous.slots and not current.slots:
            return changes

        all_slots = (
            set(previous.slots.keys())
            | set(current.slots.keys())
        )

        # Nothing to compare

        if len(all_slots) == 0:
            return changes

        for slot in sorted(all_slots):

            old = previous.slots.get(slot, "")

            new = current.slots.get(slot, "")

            if old == new:
                continue

            if old == "":
                change_type = "INSERT"

            elif new == "":
                change_type = "DELETE"

            else:
                change_type = "UPDATE"

            importance = self._calculate_importance(
                current.domain,
                slot,
                old,
                new
            )

            changes.append(

                ContextChange(

                    turn_id=current.turn_id,

                    domain=current.domain,

                    slot=slot,

                    old_value=str(old),

                    new_value=str(new),

                    change_type=change_type,

                    confidence=current.confidence,

                    importance=importance

                )

            )

        return changes

    # ---------------------------------------------------------
    # Internal Functions
    # ---------------------------------------------------------

    def _calculate_importance(
        self,
        domain,
        slot,
        old,
        new
    ) -> float:
        """
        Assign an importance score to a contextual change.

        Returns:
            float between 0.0 and 1.0
        """

        slot = slot.lower()

        # Critical booking information

        if slot in [
            "people",
            "stay",
            "day",
            "time",
            "destination",
            "departure",
            "arriveby",
            "leaveat"
        ]:
            return 1.0

        # Core user preferences

        if slot in [
            "price",
            "pricerange",
            "parking",
            "internet",
            "food",
            "area",
            "stars",
            "type"
        ]:
            return 0.8

        # Hotel / restaurant names

        if slot == "name":
            return 0.7

        # Unknown slots

        return 0.5