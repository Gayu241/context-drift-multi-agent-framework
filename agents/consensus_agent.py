"""
consensus_agent.py

Performs consensus over incoming memories.
"""

from core.memory_store import MemoryStore
from core.memory_record import MemoryRecord

from agents.conflict_detector import (
    ConflictDetector,
    ConflictType
)

from agents.consensus_policy import (
    ResearchConsensusPolicy,
    ConsensusDecision
)


class ConsensusAgent:
    """
    Resolves incoming memories against existing memory.
    """

    def __init__(self):

        self.detector = ConflictDetector()
        self.policy = ResearchConsensusPolicy()

    def process(
        self,
        store: MemoryStore,
        incoming: MemoryRecord
    ) -> ConsensusDecision:

        candidates = store.find_by_category(
            incoming.category
        )

        # No existing memories
        if not candidates:

            store.add_experience(incoming)

            return ConsensusDecision.ADD_NEW

        # Compare against every candidate
        for existing in candidates:

            conflict = self.detector.detect(
                existing,
                incoming
            )

            decision = self.policy.decide(
                existing,
                incoming,
                conflict
            )

            if decision == ConsensusDecision.KEEP_EXISTING:

                return decision

            if decision == ConsensusDecision.UPDATE_EXISTING:

                existing.update(
                    incoming.content
                )

                existing.confidence = incoming.confidence
                existing.importance = incoming.importance

                return decision

        # Independent memory

        store.add_experience(incoming)

        return ConsensusDecision.ADD_NEW