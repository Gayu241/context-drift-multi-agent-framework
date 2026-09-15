"""
drift_types.py

Defines the supported context drift scenarios.
"""

from enum import Enum


class DriftType(Enum):

    SLOT_UPDATE = "Slot Update"

    SLOT_INSERTION = "Slot Insertion"

    SLOT_DELETION = "Slot Deletion"

    CONTRADICTION = "Contradiction"

    MULTI_SLOT = "Multi Slot"

    GOAL_DRIFT = "Goal Drift"

    RANDOM = "Random"