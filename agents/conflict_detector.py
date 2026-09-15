"""
conflict_detector.py

Detects the relationship between two memories.
"""

from enum import Enum

from core.memory_record import MemoryRecord


class ConflictType(Enum):
    """
    Relationship between two memories.
    """

    DUPLICATE = "DUPLICATE"

    CONFLICT = "CONFLICT"

    INDEPENDENT = "INDEPENDENT"


class ConflictDetector:
    """
    Determines whether two memories are duplicates,
    conflicting, or independent.
    """

    def detect(
        self,
        existing: MemoryRecord,
        incoming: MemoryRecord
    ) -> ConflictType:

        existing_keys = set(existing.content.keys())
        incoming_keys = set(incoming.content.keys())

        shared_keys = existing_keys & incoming_keys

        # No shared slots
        if not shared_keys:
            return ConflictType.INDEPENDENT

        # Compare shared values
        for key in shared_keys:

            if existing.content[key] != incoming.content[key]:
                return ConflictType.CONFLICT

        # Same values for every shared slot
        if existing.content == incoming.content:
            return ConflictType.DUPLICATE

        # Same shared values but incoming contains extra slots
        return ConflictType.INDEPENDENT