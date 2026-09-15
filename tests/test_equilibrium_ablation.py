"""
test_equilibrium_ablation.py

Single-case comparison of:

1. Standard drift-level adaptation
2. Equilibrium-Based Drift Control
"""

from data.adapters.multiwoz_adapter import MultiWOZAdapter
from evaluation.experiment_preparer import ExperimentPreparer
from experiments.equilibrium_experiment_runner import (
    EquilibriumExperimentRunner
)
from drift_injection.drift_types import DriftType


DATASET_PATH = (
    "datasets/multiwoz/data/"
    "MULTIWOZ2.4/data.json"
)


def main():

    print("Loading dataset...\n")

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

    # -------------------------------------------------
    # Find a usable belief
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Prepare controlled drift
    # -------------------------------------------------

    preparer = ExperimentPreparer()

    (
        experiment,
        ground_truth,
        drifted
    ) = preparer.prepare(
        conversation,
        belief_index,
        DriftType.SLOT_UPDATE
    )

    # -------------------------------------------------
    # Store pre-drift belief for the pipeline
    # -------------------------------------------------

    if not hasattr(
        experiment,
        "metadata"
    ):

        experiment.metadata = {}

    experiment.metadata[
        "pre_drift_belief"
    ] = ground_truth

    # -------------------------------------------------
    # Run comparison
    # -------------------------------------------------

    runner = EquilibriumExperimentRunner(
        equilibrium_boundary=0.35
    )

    results = runner.run(
        experiment,
        ground_truth,
        drifted,
        DriftType.SLOT_UPDATE,
        belief_index
    )

    standard = results[
        "standard"
    ]

    equilibrium = results[
        "equilibrium"
    ]

    # -------------------------------------------------
    # Display
    # -------------------------------------------------

    print()
    print("=" * 70)
    print("EQUILIBRIUM ABLATION TEST")
    print("=" * 70)

    print()
    print("Conversation :", dialogue_id)
    print("Drift Type   :", DriftType.SLOT_UPDATE)
    print("Boundary     :", 0.35)

    print()
    print("STANDARD FRAMEWORK")
    print("-" * 70)

    print(
        f"CRS : {standard.context_retention_score:.3f}"
    )

    print(
        f"BRA : {standard.belief_revision_accuracy:.3f}"
    )

    print(
        f"HR  : {standard.hallucination_rate:.3f}"
    )

    print(
        f"ASR : {standard.adaptation_success_rate:.3f}"
    )

    print(
        f"EDS : {standard.equilibrium_deviation_score:.3f}"
    )

    print(
        f"ERR : {standard.equilibrium_recovery_rate:.3f}"
    )

    print()
    print("EQUILIBRIUM-BASED FRAMEWORK")
    print("-" * 70)

    print(
        f"CRS : {equilibrium.context_retention_score:.3f}"
    )

    print(
        f"BRA : {equilibrium.belief_revision_accuracy:.3f}"
    )

    print(
        f"HR  : {equilibrium.hallucination_rate:.3f}"
    )

    print(
        f"ASR : {equilibrium.adaptation_success_rate:.3f}"
    )

    print(
        f"EDS : {equilibrium.equilibrium_deviation_score:.3f}"
    )

    print(
        f"ERR : {equilibrium.equilibrium_recovery_rate:.3f}"
    )

    print()
    print("=" * 70)


if __name__ == "__main__":

    main()