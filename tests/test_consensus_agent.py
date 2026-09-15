from core.memory_store import MemoryStore
from core.memory_record import MemoryRecord

from agents.consensus_agent import ConsensusAgent


store = MemoryStore()

agent = ConsensusAgent()

# Existing memory

store.add_experience(

    MemoryRecord(

        category="HOTEL",

        content={
            "parking": "yes"
        },

        confidence=0.80,

        importance=0.70
    )
)

# Incoming conflicting memory

incoming = MemoryRecord(

    category="HOTEL",

    content={
        "parking": "no"
    },

    confidence=0.95,

    importance=0.90
)

decision = agent.process(
    store,
    incoming
)

print()

print("Decision")
print("----------------")
print(decision)

print()

print("Memory Store")
print("----------------")

for memory in store.experience_memory:

    print(memory)
    print(memory.content)