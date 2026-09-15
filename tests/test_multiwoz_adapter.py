from pathlib import Path
from data.adapters.multiwoz_adapter import MultiWOZAdapter

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT
    / "datasets"
    / "multiwoz"
    / "data"
    / "MULTIWOZ2.4"
    / "data.json"
)

adapter = MultiWOZAdapter(DATASET_PATH)

print("=" * 80)
print("DATASET LOADED")
print("=" * 80)

print()

dialogue_id = adapter.get_random_dialogue()

print("Random Dialogue:")
print(dialogue_id)

print()

conversation = adapter.to_conversation(dialogue_id)

print("=" * 80)
print("CONVERSATION")
print("=" * 80)

print(conversation)

print()

print("Domains")
print(conversation.domains)

print()

print("Number of Turns")
print(conversation.num_turns())

print()

print("Latest Turn")
print(conversation.latest_turn())

print()

print("Number of Belief States")
print(len(conversation.belief_states))

print()

print("Latest Belief State")
print(conversation.latest_belief_state())

print()

print("Memory")
print(conversation.memory)