"""
evaluation_result.py

Container for experimental evaluation results.
"""

from dataclasses import dataclass


@dataclass
class EvaluationResult:

    conversation_id: str

    condition: str = ""

    drift_type: str = ""

    context_retention_score: float = 0.0

    belief_revision_accuracy: float = 0.0

    agent_stability_index: float = 0.0

    contradiction_resolution_rate: float = 0.0

    hallucination_rate: float = 0.0

    adaptation_success_rate: float = 0.0

    equilibrium_deviation_score: float = 0.0

    equilibrium_recovery_rate: float = 0.0
    adaptation_action: str = ""

    # =====================================================

    def to_dict(self):

        return {

            "Conversation": self.conversation_id,

            "Condition": self.condition,

            "DriftType": self.drift_type,

            "CRS": self.context_retention_score,

            "BRA": self.belief_revision_accuracy,

            "ASI": self.agent_stability_index,

            "CRR": self.contradiction_resolution_rate,

            "HR": self.hallucination_rate,

            "ASR": self.adaptation_success_rate,

            "EDS": self.equilibrium_deviation_score,

            "ERR": self.equilibrium_recovery_rate,
            "AdaptationAction": self.adaptation_action

        }