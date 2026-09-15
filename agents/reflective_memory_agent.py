from core.memory_record import MemoryRecord
from core.cognitive_status import CognitiveStatus

from agents.memory_policy import ResearchMemoryPolicy


class ReflectiveMemoryAgent:
    """
    Reflective Memory Agent.

    Converts validated conversational knowledge into
    structured cognitive memories.
    """

    def __init__(self, policy=None):

        self.policy = policy or ResearchMemoryPolicy()

    def process(self, state):

        drift = state.drift_report
        validation = state.validation_report
        belief = state.current_belief

        decision = self.policy.decide(
            drift,
            validation
        )

        if decision in ["IGNORE", "REJECT"]:

            state.status = CognitiveStatus.MEMORY_UPDATED
            return state

        category = "GENERAL"

        if hasattr(belief, "domain"):
            category = belief.domain.upper()

        record = MemoryRecord(
            turn_id=belief.turn_id,
            category=category,
            content=belief.slots,
            importance=drift.weighted_drift_score,
            confidence=validation.confidence,
            source="ReflectiveMemoryAgent"
        )

        if decision == "SHORT_TERM":

            state.memory.add_short_term(record)

        elif decision == "REFLECTION":

            state.memory.add_reflection(record)

        elif decision == "EXPERIENCE":

            state.memory.add_experience(record)

        state.status = CognitiveStatus.MEMORY_UPDATED

        return state