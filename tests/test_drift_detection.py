from agents.context_monitoring_agent import ContextMonitoringAgent
from agents.drift_detection_agent import DriftDetectionAgent
from core.belief_state import BeliefState


previous = BeliefState(
    turn_id=1,
    domain="hotel",
    slots={
        "parking": "not mentioned",
        "pricerange": "cheap",
        "internet": "no"
    }
)

current = BeliefState(
    turn_id=2,
    domain="hotel",
    slots={
        "parking": "yes",
        "pricerange": "expensive",
        "internet": "yes",
        "people": "4"
    }
)

monitor = ContextMonitoringAgent()

changes = monitor.monitor(previous, current)

all_slots = (
    set(previous.slots.keys())
    |
    set(current.slots.keys())
)

total_slots = len(all_slots)

print("=" * 80)
print("Context Changes")
print("=" * 80)

for change in changes:
    print(change)

drift_agent = DriftDetectionAgent()

report = drift_agent.detect(
    changes,
    total_slots
)

print("\n")
print("=" * 80)
print("Drift Report")
print("=" * 80)

print(report)