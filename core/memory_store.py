"""
memory_store.py

Stores and retrieves cognitive memories.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from core.memory_record import MemoryRecord


@dataclass
class MemoryStore:
    """
    Stores memories using three cognitive layers.

    Short-Term Memory
    Reflection Queue
    Experience Memory
    """

    short_term: List[MemoryRecord] = field(default_factory=list)

    reflection_queue: List[MemoryRecord] = field(default_factory=list)

    experience_memory: List[MemoryRecord] = field(default_factory=list)

    # =====================================================
    # Add Memory
    # =====================================================

    def add_short_term(self, record: MemoryRecord):

        self.short_term.append(record)

    def add_reflection(self, record: MemoryRecord):

        self.reflection_queue.append(record)

    def add_experience(self, record: MemoryRecord):

        self.experience_memory.append(record)

    # =====================================================
    # Retrieval
    # =====================================================

    def all_memories(self) -> List[MemoryRecord]:
        """
        Returns every memory in the system.
        """

        return (
            self.short_term +
            self.reflection_queue +
            self.experience_memory
        )

    def find_by_memory_id(self, memory_id: str) -> Optional[MemoryRecord]:
        """
        Find a memory by its unique ID.
        """

        for memory in self.all_memories():

            if memory.memory_id == memory_id:
                return memory

        return None

    def find_by_category(self, category: str) -> List[MemoryRecord]:
        """
        Return all memories belonging to a category.
        """

        return [
            memory
            for memory in self.all_memories()
            if memory.category == category
        ]

    def find_recent(self, n: int = 5) -> List[MemoryRecord]:
        """
        Return the most recently updated memories.
        """

        memories = sorted(
            self.all_memories(),
            key=lambda x: x.last_updated,
            reverse=True
        )

        return memories[:n]

    # =====================================================
    # Utility
    # =====================================================

    def clear(self):

        self.short_term.clear()
        self.reflection_queue.clear()
        self.experience_memory.clear()

    def summary(self):

        return {
            "short_term": len(self.short_term),
            "reflection_queue": len(self.reflection_queue),
            "experience_memory": len(self.experience_memory),
            "total": len(self.all_memories())
        }