"""
test_experiment_preparer.py

Tests the ExperimentPreparer by selecting the first
meaningful belief state from a random MultiWOZ dialogue.
"""
from drift_injection.drift_types import DriftType
from data.adapters.multiwoz_adapter import MultiWOZAdapter
from evaluation.experiment_preparer import ExperimentPreparer


def main():

    print("Loading dataset...\n")

    adapter = MultiWOZAdapter(
        "datasets/multiwoz/data/MULTIWOZ2.4/data.json"
    )

    dialogue_id = adapter.get_random_dialogue()

    conversation = adapter.to_conversation(dialogue_id)

    print(f"Dialogue : {dialogue_id}")
    print(f"Beliefs  : {len(conversation.belief_states)}")

    # ------------------------------------------------------
    # Find first non-empty belief state
    # ------------------------------------------------------

    belief_index = None

    for i, belief in enumerate(conversation.belief_states):

        if belief.slots:

            belief_index = i
            break

    if belief_index is None:

        print("\nNo non-empty belief state found.")
        return

    # ------------------------------------------------------

    preparer = ExperimentPreparer()

    experiment, ground_truth, drifted = preparer.prepare(
        conversation=conversation,
        belief_index=belief_index,
        drift_type=DriftType.SLOT_DELETION
    )

    print("\n========================================")
    print("EXPERIMENT PREPARATION")
    print("========================================")

    print(f"\nBelief Index : {belief_index}")

    print("\nGround Truth")
    print("-----------------------")
    print("Domain :", ground_truth.domain)
    print("Slots  :", ground_truth.slots)

    print("\nDrifted")
    print("-----------------------")
    print("Domain :", drifted.domain)
    print("Slots  :", drifted.slots)

    print("\nConversation Check")
    print("-----------------------")
    print(
        experiment.belief_states[belief_index].slots
    )

    print("\n✅ Experiment prepared successfully.")


if __name__ == "__main__":
    main()