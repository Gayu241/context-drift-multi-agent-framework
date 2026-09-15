from dataclasses import dataclass, field

from core.memory_store import MemoryStore
from core.memory_record import MemoryRecord


@dataclass
class Memory:
    """
    High-level interface to the cognitive memory system.
    """

    store: MemoryStore = field(default_factory=MemoryStore)

    # =====================================================
    # Memory Operations
    # =====================================================

    def add_short_term(self, record: MemoryRecord):

        self.store.add_short_term(record)

    def add_reflection(self, record: MemoryRecord):

        self.store.add_reflection(record)

    def add_experience(self, record: MemoryRecord):

        self.store.add_experience(record)

    # =====================================================
    # Utility
    # =====================================================

    def summary(self):

        return self.store.summary()

    def clear(self):

        self.store.short_term.clear()
        self.store.reflection_queue.clear()
        self.store.experience_memory.clear()

    def __str__(self):

        stats = self.summary()

        return (
            f"Memory("
            f"STM={stats['short_term']}, "
            f"Reflection={stats['reflection_queue']}, "
            f"Experience={stats['experience_memory']})"
        )