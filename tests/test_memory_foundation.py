from core.memory_record import MemoryRecord
from core.memory_store import MemoryStore

memory = MemoryStore()

record = MemoryRecord(
    turn_id=3,
    category="HOTEL",
    content={
        "parking": "yes",
        "internet": "yes"
    },
    importance=0.8,
    confidence=0.95,
    source="BeliefValidation"
)

memory.add_short_term(record)

print(record)
print(memory.summary())

record.update({
    "wifi": "free"
})

print()
print("After Update")
print(record)
print(record.content)