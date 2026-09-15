from agents.belief_validation_agent import BeliefValidationAgent
from core.belief_state import BeliefState


belief = BeliefState(
    turn_id=5,
    domain="hotel",
    slots={
        "people": "4",
        "stay": "2",
        "parking": "yes",
        "internet": "yes",
        "pricerange": "cheap"
    }
)

agent = BeliefValidationAgent()

report = agent.validate(belief)

print("=" * 80)
print("Validation Report")
print("=" * 80)

print(report)

if report.issues:
    print("\nIssues:")
    for issue in report.issues:
        print("-", issue)