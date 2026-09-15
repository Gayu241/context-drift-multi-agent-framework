from core.conversation import Conversation
from core.cognitive_state import CognitiveState
from core.memory import Memory
from core.belief_state import BeliefState
from core.drift_report import DriftReport
from core.validation_report import ValidationReport

from agents.reflective_memory_agent import ReflectiveMemoryAgent


# ---------------------------------------------------
# Create a dummy conversation
# ---------------------------------------------------

conversation = Conversation(
    conversation_id="TEST001",
    dataset="UnitTest"
)

# ---------------------------------------------------
# Create a belief state
# ---------------------------------------------------

belief = BeliefState(
    turn_id=5,
    domain="hotel",
    slots={
        "parking": "yes",
        "internet": "yes"
    }
)

# ---------------------------------------------------
# Create a drift report
# ---------------------------------------------------

drift = DriftReport(
    turn_id=5,
    drift_score=0.75,
    weighted_drift_score=0.82,
    equilibrium_score=0.80,
    drift_level="HIGH_DRIFT",
    context_changes=[]
)

# ---------------------------------------------------
# Create a validation report
# ---------------------------------------------------

validation = ValidationReport(
    turn_id=5,
    is_valid=True,
    confidence=0.96,
    issues=[],
    validated_slots=2
)

# ---------------------------------------------------
# Create Cognitive State
# ---------------------------------------------------

state = CognitiveState(
    conversation=conversation
)

state.current_belief = belief
state.drift_report = drift
state.validation_report = validation
state.memory = Memory()

# ---------------------------------------------------
# Run Reflective Memory Agent
# ---------------------------------------------------

agent = ReflectiveMemoryAgent()

state = agent.process(state)

# ---------------------------------------------------
# Display Results
# ---------------------------------------------------

print("\nMemory Summary")
print("----------------")

print(state.memory.summary())

print()

print(state.memory)