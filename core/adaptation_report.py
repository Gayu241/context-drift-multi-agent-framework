from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from core.adaptation_action import AdaptationAction


@dataclass
class AdaptationReport:
    """
    Stores the output produced by the Response Adaptation Policy.
    """

    action: AdaptationAction
    reason: str

    confidence: float = 1.0

    goal_available: bool = False
    memory_available: bool = False
    belief_valid: bool = True

    metadata: Dict[str, Any] = field(default_factory=dict)

    def summary(self) -> Dict[str, Any]:
        return {
            "action": self.action.value,
            "reason": self.reason,
            "confidence": self.confidence,
            "goal_available": self.goal_available,
            "memory_available": self.memory_available,
            "belief_valid": self.belief_valid
        }

    def __str__(self):

        return (
            f"AdaptationReport("
            f"action={self.action.value}, "
            f"reason='{self.reason}', "
            f"confidence={self.confidence:.2f})"
        )