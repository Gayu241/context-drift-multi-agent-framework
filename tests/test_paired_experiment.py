"""
test_paired_experiment.py

Quick sanity test for the paired
baseline-vs-proposed experiment.
"""

from data.adapters.multiwoz_adapter import (
    MultiWOZAdapter
)

from experiments.experiment_runner import (
    ExperimentRunner
)

from drift_injection.drift_types import (
    DriftType
)


DATASET_PATH = (
    "datasets/multiwoz/data/"
    "MULTIWOZ2.4/data.json"
)


def main():

    print(
        "Loading dataset...\n"
    )

    adapter = MultiWOZAdapter(
        DATASET_PATH
    )

    dialogue_id = (
        adapter.get_random_dialogue()
    )

    conversation = (
        adapter.to_conversation(
            dialogue_id
        )
    )

    belief_index = None

    for i, belief in enumerate(
        conversation.belief_states
    ):

        if belief.slots:

            belief_index = i

            break

    if belief_index is None:

        raise RuntimeError(
            "No valid belief state found."
        )

    runner = ExperimentRunner()

    result = runner.run(

        conversation,

        belief_index,

        DriftType.SLOT_UPDATE

    )

    baseline = result[
        "baseline"
    ]

    proposed = result[
        "proposed"
    ]

    # =================================================
    # OUTPUT
    # =================================================

    print()
    print("=" * 60)
    print("PAIRED EXPERIMENT")
    print("=" * 60)

    print()
    print("Conversation")
    print("----------------")
    print(
        conversation.conversation_id
    )

    print()
    print("Drift Type")
    print("----------------")
    print(
        DriftType.SLOT_UPDATE
    )

    # =================================================
    # BASELINE
    # =================================================

    print()
    print("BASELINE")
    print("----------------")

    print(
        f"CRS : "
        f"{baseline.context_retention_score:.3f}"
    )

    print(
        f"BRA : "
        f"{baseline.belief_revision_accuracy:.3f}"
    )

    print(
        f"HR  : "
        f"{baseline.hallucination_rate:.3f}"
    )

    print(
        f"EDS : "
        f"{baseline.equilibrium_deviation_score:.3f}"
    )

    print(
        f"ERR : "
        f"{baseline.equilibrium_recovery_rate:.3f}"
    )

    # =================================================
    # PROPOSED
    # =================================================

    print()
    print("PROPOSED FRAMEWORK")
    print("----------------")

    print(
        f"CRS : "
        f"{proposed.context_retention_score:.3f}"
    )

    print(
        f"BRA : "
        f"{proposed.belief_revision_accuracy:.3f}"
    )

    print(
        f"HR  : "
        f"{proposed.hallucination_rate:.3f}"
    )

    print(
        f"ASR : "
        f"{proposed.adaptation_success_rate:.3f}"
    )

    print(
        f"EDS : "
        f"{proposed.equilibrium_deviation_score:.3f}"
    )

    print(
        f"ERR : "
        f"{proposed.equilibrium_recovery_rate:.3f}"
    )

    # =================================================
    # IMPROVEMENT
    # =================================================

    print()
    print("IMPROVEMENT")
    print("----------------")

    print(
        f"BRA improvement : "
        f"{proposed.belief_revision_accuracy - baseline.belief_revision_accuracy:.3f}"
    )

    print(
        f"CRS improvement : "
        f"{proposed.context_retention_score - baseline.context_retention_score:.3f}"
    )

    print(
        f"HR change       : "
        f"{proposed.hallucination_rate - baseline.hallucination_rate:.3f}"
    )

    print()
    print("=" * 60)


if __name__ == "__main__":

    main()