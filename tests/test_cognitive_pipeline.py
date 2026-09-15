import os
import sys

# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from data.adapters.multiwoz_adapter import MultiWOZAdapter
from pipeline.cognitive_pipeline import CognitivePipeline

# ---------------------------------------------------------


def main():

    print("=" * 80)
    print("CONTEXT DRIFT COGNITIVE PIPELINE TEST")
    print("=" * 80)

    # -----------------------------------------------------
    # Load MultiWOZ
    # -----------------------------------------------------

    print("\nLoading MultiWOZ dataset...\n")

    adapter = MultiWOZAdapter(
        "datasets/multiwoz/data/MULTIWOZ2.4/data.json"
    )

    # -----------------------------------------------------
    # Select a random dialogue
    # -----------------------------------------------------

    dialogue_id = adapter.get_random_dialogue()

    print(f"Dialogue ID : {dialogue_id}")

    conversation = adapter.to_conversation(dialogue_id)

    print(f"Dataset     : {conversation.dataset}")
    print(f"Domains     : {conversation.domains}")
    print(f"Turns       : {len(conversation.turns)}")
    print(f"Beliefs     : {len(conversation.belief_states)}")

    # -----------------------------------------------------
    # Run pipeline
    # -----------------------------------------------------

    print("\nRunning Cognitive Pipeline...\n")

    print("\n========== LAST 10 BELIEF STATES ==========\n")

    for belief in conversation.belief_states[-10:]:
        print(
            f"Turn={belief.turn_id:2d}",
            f"Domain={belief.domain:12s}",
            belief.slots
    )

    print()

    pipeline = CognitivePipeline()

    state = pipeline.run(conversation)

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print("\n")

    pipeline.summary(state)

    print("\n")

    print("=" * 80)
    print("FINAL STATE")
    print("=" * 80)

    print("Conversation ID :", state.conversation.conversation_id)
    print("Dataset         :", state.conversation.dataset)
    print("Status          :", state.status)

    if state.current_belief:

        print("\nCurrent Belief")

        print("----------------")

        print("Domain :", state.current_belief.domain)
        print("Slots  :", state.current_belief.slots)

    if state.drift_report:

        print("\nDrift Report")

        print("----------------")

        print("Level :", state.drift_report.drift_level)
        print(state.drift_report)

    if state.validation_report:

        print("\nValidation Report")

        print("------------------")

        print("Valid :", state.validation_report.is_valid)
        print(state.validation_report)

    if hasattr(state, "adaptation_report") and state.adaptation_report:

        print("\nAdaptation Report")

        print("------------------")

        print("Action :", state.adaptation_report.action)
        print(state.adaptation_report)

    print("\nMemory Summary")

    print("----------------")

    print(state.memory.summary())

    if hasattr(state, "metadata"):

        print("\nMetadata")

        print("----------------")

        for key, value in state.metadata.items():
            print(f"{key}: {value}")

    print("\nHistory")
    print("----------------")

    print("Belief History      :", len(state.belief_history))
    print("Drift History       :", len(state.drift_history))
    print("Validation History  :", len(state.validation_history))
    print("Adaptation History  :", len(state.adaptation_history))        

    print("\n")

    print("=" * 80)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    main()