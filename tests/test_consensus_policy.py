from agents.conflict_detector import (
    ConflictDetector,
    ConflictType
)

from agents.consensus_policy import (
    ResearchConsensusPolicy,
    ConsensusDecision
)

from core.memory_record import MemoryRecord


detector = ConflictDetector()
policy = ResearchConsensusPolicy()


# Existing memory
existing = MemoryRecord(
    category="HOTEL",
    content={
        "parking": "yes"
    },
    confidence=0.80,
    importance=0.70
)


# Incoming memory
incoming = MemoryRecord(
    category="HOTEL",
    content={
        "parking": "no"
    },
    confidence=0.95,
    importance=0.80
)


conflict = detector.detect(
    existing,
    incoming
)

print("Conflict")
print(conflict)

decision = policy.decide(
    existing,
    incoming,
    conflict
)

print()
print("Decision")
print(decision)

assert conflict == ConflictType.CONFLICT
assert decision == ConsensusDecision.UPDATE_EXISTING

print()
print("Consensus Policy Test Passed")