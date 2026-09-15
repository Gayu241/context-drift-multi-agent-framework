"""
consensus_policy.py

Determines how conflicting memories should be resolved.
"""

from abc import ABC, abstractmethod
from enum import Enum

from core.memory_record import MemoryRecord
from agents.conflict_detector import ConflictType


class ConsensusDecision(Enum):
    KEEP_EXISTING = "KEEP_EXISTING"
    UPDATE_EXISTING = "UPDATE_EXISTING"
    ADD_NEW = "ADD_NEW"


class ConsensusPolicy(ABC):

    @abstractmethod
    def decide(
        self,
        existing: MemoryRecord,
        incoming: MemoryRecord,
        conflict_type: ConflictType
    ) -> ConsensusDecision:
        """
        Decide how to handle an incoming memory.
        """
        pass


class ResearchConsensusPolicy(ConsensusPolicy):
    """
    Rule-based consensus policy.
    """

    def decide(
        self,
        existing: MemoryRecord,
        incoming: MemoryRecord,
        conflict_type: ConflictType
    ) -> ConsensusDecision:

        # Duplicate memory
        if conflict_type == ConflictType.DUPLICATE:
            return ConsensusDecision.KEEP_EXISTING

        # Independent memory
        if conflict_type == ConflictType.INDEPENDENT:
            return ConsensusDecision.ADD_NEW

        # Conflict resolution

        if incoming.confidence > existing.confidence:
            return ConsensusDecision.UPDATE_EXISTING

        if incoming.confidence < existing.confidence:
            return ConsensusDecision.KEEP_EXISTING

        if incoming.importance > existing.importance:
            return ConsensusDecision.UPDATE_EXISTING

        if incoming.importance < existing.importance:
            return ConsensusDecision.KEEP_EXISTING

        if incoming.last_updated > existing.last_updated:
            return ConsensusDecision.UPDATE_EXISTING

        return ConsensusDecision.KEEP_EXISTING