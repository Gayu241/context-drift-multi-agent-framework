"""
test_all_drift_types.py

Runs one controlled paired experiment for each
supported context-drift type.

SANITY CHECK ONLY.
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


def find_conversation_with_belief(adapter):

    for _ in range(100):

        dialogue_id = (
            adapter.get_random_dialogue()
        )

        conversation = (
            adapter.to_conversation(
                dialogue_id
            )
        )

        for i, belief in enumerate(
            conversation.belief_states
        ):

            if belief.slots:

                return (
                    conversation,
                    i
                )

    return None, None


def get_metrics(result):

    return {
        "CRS": result.context_retention_score,
        "BRA": result.belief_revision_accuracy,
        "ASI": result.agent_stability_index,
        "CRR": result.contradiction_resolution_rate,
        "HR": result.hallucination_rate,
        "ASR": result.adaptation_success_rate,
        "EDS": result.equilibrium_deviation_score,
        "ERR": result.equilibrium_recovery_rate
    }


def main():

    print("=" * 70)
    print("DRIFT TYPE SANITY CHECK")
    print("=" * 70)

    # =================================================
    # LOAD DATASET
    # =================================================

    print("\nLoading dataset...\n")

    adapter = MultiWOZAdapter(
        DATASET_PATH
    )

    print(
        "Dataset loaded successfully."
    )

    runner = ExperimentRunner()

    # =================================================
    # DRIFT TYPES
    # =================================================

    drift_types = [

        DriftType.SLOT_UPDATE,

        DriftType.SLOT_INSERTION,

        DriftType.SLOT_DELETION,

        DriftType.CONTRADICTION,

        DriftType.MULTI_SLOT,

        DriftType.GOAL_DRIFT

    ]

    results = []

    # =================================================
    # RUN SANITY CHECKS
    # =================================================

    for drift_type in drift_types:

        print("\n")
        print("=" * 70)
        print(
            "TESTING DRIFT TYPE:",
            drift_type
        )
        print("=" * 70)

        conversation, belief_index = (
            find_conversation_with_belief(
                adapter
            )
        )

        if conversation is None:

            print(
                "❌ No suitable conversation found."
            )

            continue

        print(
            "Conversation :",
            conversation.conversation_id
        )

        print(
            "Belief Index :",
            belief_index
        )

        try:

            result = runner.run(
                conversation,
                belief_index,
                drift_type
            )

            baseline = result["baseline"]
            proposed = result["proposed"]

            b = get_metrics(baseline)
            p = get_metrics(proposed)

            print("\n")
            print(
                "---------------- RESULT ----------------"
            )

            print(
                "Baseline CRS :",
                round(b["CRS"], 3)
            )

            print(
                "Baseline BRA :",
                round(b["BRA"], 3)
            )

            print(
                "Baseline HR  :",
                round(b["HR"], 3)
            )

            print(
                "Proposed CRS :",
                round(p["CRS"], 3)
            )

            print(
                "Proposed BRA :",
                round(p["BRA"], 3)
            )

            print(
                "Proposed HR  :",
                round(p["HR"], 3)
            )

            print(
                "Proposed ASR :",
                round(p["ASR"], 3)
            )

            print(
                "Proposed EDS :",
                round(p["EDS"], 3)
            )

            print(
                "Proposed ERR :",
                round(p["ERR"], 3)
            )

            print(
                "-----------------------------------------"
            )

            results.append({
                "drift_type": str(
                    drift_type
                ),
                "conversation": (
                    conversation.conversation_id
                ),
                "baseline": b,
                "proposed": p
            })

        except Exception as e:

            print()
            print(
                "❌ FAILED:",
                drift_type
            )

            print(
                type(e).__name__,
                ":",
                e
            )

    # =================================================
    # FINAL SUMMARY
    # =================================================

    print("\n\n")
    print("=" * 70)
    print("SANITY CHECK SUMMARY")
    print("=" * 70)

    for result in results:

        b = result["baseline"]
        p = result["proposed"]

        print()
        print(
            result["drift_type"]
        )

        print(
            "Conversation:",
            result["conversation"]
        )

        print(
            "CRS:",
            round(b["CRS"], 3),
            "→",
            round(p["CRS"], 3)
        )

        print(
            "BRA:",
            round(b["BRA"], 3),
            "→",
            round(p["BRA"], 3)
        )

        print(
            "HR :",
            round(b["HR"], 3),
            "→",
            round(p["HR"], 3)
        )

        print(
            "ASR:",
            round(p["ASR"], 3)
        )

        print(
            "EDS:",
            round(p["EDS"], 3)
        )

        print(
            "ERR:",
            round(p["ERR"], 3)
        )

    print("\n")
    print("=" * 70)
    print("SANITY CHECK COMPLETED")
    print("=" * 70)


if __name__ == "__main__":

    main()