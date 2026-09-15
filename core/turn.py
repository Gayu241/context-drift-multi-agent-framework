"""
turn.py

Represents a single conversational turn within the unified
conversation framework.

Each dataset (MultiWOZ, PersonaChat, DailyDialog) will be
converted into this common representation.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Turn:
    """
    Represents a single conversational turn.
    """

    # -------------------------
    # Turn Information
    # -------------------------

    turn_id: int

    speaker: str

    utterance: str

    # -------------------------
    # Optional Annotations
    # -------------------------

    dialogue_act: str = ""

    emotion: str = ""

    intent: str = ""

    # -------------------------
    # Named Entities
    # -------------------------

    entities: List[str] = field(default_factory=list)

    # -------------------------
    # Dataset-Specific Metadata
    # -------------------------

    metadata: Dict = field(default_factory=dict)

    # ==========================================================
    # Helper Functions
    # ==========================================================

    def add_entity(self, entity: str) -> None:
        """
        Add a named entity to the turn.
        """
        self.entities.append(entity)

    def has_entities(self) -> bool:
        """
        Check whether any entities are present.
        """
        return len(self.entities) > 0

    def has_emotion(self) -> bool:
        """
        Check whether the turn contains an emotion label.
        """
        return self.emotion != ""

    def has_dialogue_act(self) -> bool:
        """
        Check whether a dialogue act exists.
        """
        return self.dialogue_act != ""

    def __str__(self) -> str:
        return (
            f"Turn("
            f"id={self.turn_id}, "
            f"speaker={self.speaker}, "
            f'utterance="{self.utterance[:50]}..."'
            f")"
        )