"""
drift_scenarios.py

Predefined experimental drift scenarios.
"""

from drift_injection.drift_types import DriftType


SCENARIOS = {

    "Scenario 1": [
        DriftType.SLOT_UPDATE
    ],

    "Scenario 2": [
        DriftType.CONTRADICTION
    ],

    "Scenario 3": [
        DriftType.SLOT_INSERTION
    ],

    "Scenario 4": [
        DriftType.SLOT_DELETION
    ],

    "Scenario 5": [
        DriftType.MULTI_SLOT
    ],

    "Scenario 6": [
        DriftType.GOAL_DRIFT
    ],

    "Scenario 7": [
        DriftType.RANDOM
    ]
}