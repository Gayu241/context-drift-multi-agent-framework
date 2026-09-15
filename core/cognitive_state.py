"""
Shared cognitive state exchanged between all processing modules.
"""

from dataclasses import dataclass, field
from typing import Optional, List

from core.conversation import Conversation
from core.belief_state import BeliefState
from core.context_change import ContextChange
from core.drift_report import DriftReport
from core.validation_report import ValidationReport
from core.memory import Memory
from core.cognitive_status import CognitiveStatus


@dataclass
class CognitiveState:
    """
    Shared state of the cognitive architecture.
    """

    # =====================================================
    # Conversation
    # =====================================================

    conversation: Conversation

    # =====================================================
    # Current Belief
    # =====================================================

    current_belief: Optional[BeliefState] = None

    # =====================================================
    # Context Monitoring
    # =====================================================

    context_changes: List[ContextChange] = field(default_factory=list)

    # =====================================================
    # Drift Detection
    # =====================================================

    drift_report: Optional[DriftReport] = None

    # =====================================================
    # Validation
    # =====================================================

    validation_report: Optional[ValidationReport] = None

    # =====================================================
    # Conversation History
    # =====================================================

    belief_history: list = field(default_factory=list)

    drift_history: list = field(default_factory=list)

    validation_history: list = field(default_factory=list)

    adaptation_history: list = field(default_factory=list)



    # =====================================================
    # Memory
    # =====================================================

    memory: Memory = field(default_factory=Memory)

    # =====================================================
    # Response Adaptation
    # =====================================================

    adaptation_report = None

    # =====================================================
    # Runtime Metadata
    # =====================================================

    metadata: dict = field(default_factory=dict)

    # =====================================================
    # Status
    # =====================================================

    status: CognitiveStatus = CognitiveStatus.INITIALIZED

    def __str__(self):

        memory = self.memory.summary()

        return (
            "\n"
            "==============================\n"
            " Cognitive State\n"
            "==============================\n"
            f"Conversation : {self.conversation.conversation_id}\n"
            f"Dataset      : {self.conversation.dataset}\n"
            f"Belief       : {self.current_belief is not None}\n"
            f"Changes      : {len(self.context_changes)}\n"
            f"Drift        : {self.drift_report is not None}\n"
            f"Validation   : {self.validation_report is not None}\n"
            f"STM          : {memory['short_term']}\n"
            f"Reflection   : {memory['reflection_queue']}\n"
            f"Experience   : {memory['experience_memory']}\n"
            f"Status       : {self.status.value}\n"
        )