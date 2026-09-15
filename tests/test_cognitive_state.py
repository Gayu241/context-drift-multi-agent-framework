from pathlib import Path

from data.adapters.multiwoz_adapter import MultiWOZAdapter

from agents.context_monitoring_agent import ContextMonitoringAgent
from agents.drift_detection_agent import DriftDetectionAgent
from agents.belief_validation_agent import BeliefValidationAgent
from agents.cognitive_state_manager import CognitiveStateManager


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

dialogue_id = adapter.list_dialogue_ids()[0]

conversation = adapter.to_conversation(dialogue_id)

beliefs = conversation.belief_states

previous = beliefs[0]
current = beliefs[1]

monitor = ContextMonitoringAgent()

changes = monitor.monitor(previous, current)

all_slots = (
    set(previous.slots.keys())
    |
    set(current.slots.keys())
)

drift = DriftDetectionAgent().detect(
    changes,
    len(all_slots)
)

validation = BeliefValidationAgent().validate(current)

manager = CognitiveStateManager()

state = manager.initialize(conversation)

manager.update_belief(state, current)
manager.update_changes(state, changes)
manager.update_drift(state, drift)
manager.update_validation(state, validation)

manager.finalize(state)

print(state)
print(previous.slots)
print()

print(current.slots)