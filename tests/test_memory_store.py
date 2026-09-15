from core.memory_store import MemoryStore
from core.memory_record import MemoryRecord


store = MemoryStore()

store.add_short_term(
    MemoryRecord(
        turn_id=1,
        category="HOTEL",
        content={"parking": "yes"}
    )
)

store.add_experience(
    MemoryRecord(
        turn_id=5,
        category="HOTEL",
        content={"internet": "yes"}
    )
)

store.add_experience(
    MemoryRecord(
        turn_id=7,
        category="TRAIN",
        content={"destination": "Cambridge"}
    )
)

print()

print("Summary")
print(store.summary())

print()

print("Hotel Memories")
print("----------------")

for memory in store.find_by_category("HOTEL"):
    print(memory)

print()

print("Recent Memories")
print("----------------")

for memory in store.find_recent():
    print(memory)