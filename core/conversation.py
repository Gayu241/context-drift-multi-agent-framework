"""
conversation.py

Unified conversation object used across all datasets
(MultiWOZ, PersonaChat, DailyDialog).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from core.turn import Turn
from core.belief_state import BeliefState


@dataclass
class Conversation:
    """
    Unified conversation representation.
    """

    # ==========================================================
    # Basic Information
    # ==========================================================

    conversation_id: str
    dataset: str

    # ==========================================================
    # Dataset Information
    # ==========================================================

    domains: List[str] = field(default_factory=list)

    persona: List[str] = field(default_factory=list)

    goal: Dict = field(default_factory=dict)

    # ==========================================================
    # Conversation Content
    # ==========================================================

    turns: List[Turn] = field(default_factory=list)

    belief_states: List[BeliefState] = field(default_factory=list)

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata: Dict = field(default_factory=dict)

    embeddings: Optional[List[float]] = None

    # ==========================================================
    # Helper Methods
    # ==========================================================

    def add_turn(self, turn: Turn):

        self.turns.append(turn)

    def add_belief_state(self, belief_state: BeliefState):

        self.belief_states.append(belief_state)

    def latest_turn(self):

        if self.turns:
            return self.turns[-1]

        return None

    def latest_belief_state(self):

        if self.belief_states:
            return self.belief_states[-1]

        return None

    def active_domains(self):

        return self.domains

    def num_turns(self):

        return len(self.turns)

    def has_persona(self):

        return len(self.persona) > 0

    def has_goal(self):

        return len(self.goal) > 0

    def __str__(self):

        return (
            f"Conversation("
            f"id={self.conversation_id}, "
            f"dataset={self.dataset}, "
            f"turns={len(self.turns)}, "
            f"domains={self.domains})"
        )