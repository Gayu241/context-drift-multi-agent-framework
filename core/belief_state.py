"""
belief_state.py

Represents the conversational belief state at a given turn.

A belief state captures the system's current understanding of
the user's goals, constraints, preferences, and booking
information.

This class is primarily populated from MultiWOZ but is designed
to remain generic for future datasets.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class BeliefState:
    """
    Represents the belief state at a specific conversation turn.
    """

    # -------------------------
    # General Information
    # -------------------------

    turn_id: int

    domain: str

    # -------------------------
    # Dialogue State
    # -------------------------

    slots: Dict[str, str] = field(default_factory=dict)

    booking: Dict[str, str] = field(default_factory=dict)

    # -------------------------
    # Confidence
    # -------------------------

    confidence: float = 1.0

    # -------------------------
    # Additional Metadata
    # -------------------------

    metadata: Dict = field(default_factory=dict)

    # ==========================================================
    # Helper Functions
    # ==========================================================

    def update_slot(self, slot: str, value: str) -> None:
        """
        Update or add a slot-value pair.
        """
        self.slots[slot] = value

    def update_booking(self, key: str, value: str) -> None:
        """
        Update booking information.
        """
        self.booking[key] = value

    def get_slot(self, slot: str) -> Optional[str]:
        """
        Retrieve a slot value.
        """
        return self.slots.get(slot)

    def has_slot(self, slot: str) -> bool:
        """
        Check whether a slot exists.
        """
        return slot in self.slots

    def remove_slot(self, slot: str) -> None:
        """
        Remove a slot if present.
        """
        self.slots.pop(slot, None)

    def num_slots(self) -> int:
        """
        Return the number of active slots.
        """
        return len(self.slots)

    def is_empty(self) -> bool:
        """
        Check whether the belief state contains any information.
        """
        return len(self.slots) == 0 and len(self.booking) == 0

    def __str__(self) -> str:
        return (
            f"BeliefState("
            f"turn={self.turn_id}, "
            f"domain={self.domain}, "
            f"slots={len(self.slots)}, "
            f"booking={len(self.booking)})"
        )