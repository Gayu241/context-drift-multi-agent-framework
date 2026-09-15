"""
memory_record.py

Represents a single cognitive memory stored by the framework.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict
import uuid


@dataclass
class MemoryRecord:
    """
    Represents a validated memory stored by the framework.

    Every memory receives a unique identifier so that future
    agents (Consensus, Adaptation, etc.) can reference and
    update existing memories instead of creating duplicates.
    """

    # =====================================================
    # Identity
    # =====================================================

    memory_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    version: int = 1

    # =====================================================
    # Origin
    # =====================================================

    turn_id: int = 0

    category: str = "GENERAL"

    source: str = "Unknown"

    # =====================================================
    # Memory Content
    # =====================================================

    content: Dict[str, Any] = field(default_factory=dict)

    # =====================================================
    # Quality Metrics
    # =====================================================

    importance: float = 1.0

    confidence: float = 1.0

    # =====================================================
    # Timestamps
    # =====================================================

    created_at: datetime = field(default_factory=datetime.now)

    last_updated: datetime = field(default_factory=datetime.now)

    # =====================================================
    # Additional Metadata
    # =====================================================

    metadata: Dict[str, Any] = field(default_factory=dict)

    # =====================================================
    # Methods
    # =====================================================

    def update(self, new_content: Dict[str, Any]):
        """
        Update an existing memory.
        """

        self.content.update(new_content)
        self.version += 1
        self.last_updated = datetime.now()

    def __str__(self):

        return (
            f"[Memory {self.memory_id[:8]}] "
            f"{self.category} "
            f"(v{self.version}, "
            f"importance={self.importance:.2f}, "
            f"confidence={self.confidence:.2f})"
        )