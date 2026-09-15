from agents.context_monitoring_agent import ContextMonitoringAgent
from core.belief_state import BeliefState


previous = BeliefState(
    turn_id=1,
    domain="hotel",
    slots={
        "parking": "not mentioned",
        "pricerange": "cheap"
    }
)

current = BeliefState(
    turn_id=3,
    domain="hotel",
    slots={
        "parking": "yes",
        "pricerange": "cheap",
        "internet": "yes",
        "people": "4"
    }
)

agent = ContextMonitoringAgent()

changes = agent.monitor(previous, current)

print("=" * 80)

print("Detected Context Changes")

print("=" * 80)

for change in changes:
    print(change)