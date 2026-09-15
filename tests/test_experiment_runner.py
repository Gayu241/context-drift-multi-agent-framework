"""
test_experiment_runner.py
"""

from data.adapters.multiwoz_adapter import MultiWOZAdapter

from experiments.experiment_runner import ExperimentRunner

from drift_injection.drift_types import DriftType


def main():

    print("Loading dataset...\n")

    adapter = MultiWOZAdapter(
        "datasets/multiwoz/data/MULTIWOZ2.4/data.json"
    )

    dialogue = adapter.get_random_dialogue()

    conversation = adapter.to_conversation(
        dialogue
    )

    belief_index = None

    for i, belief in enumerate(
        conversation.belief_states
    ):

        if belief.slots:

            belief_index = i

            break

    runner = ExperimentRunner()

    result = runner.run(

        conversation,

        belief_index,

        DriftType.SLOT_DELETION

    )

    print()

    print("=" * 60)

    print("EXPERIMENT RESULT")

    print("=" * 60)

    print(result)

    print("=" * 60)


if __name__ == "__main__":

    main()