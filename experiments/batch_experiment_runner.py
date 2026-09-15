"""
batch_experiment_runner.py

Runs paired baseline-vs-proposed experiments
across MultiWOZ.

Each conversation can be evaluated under multiple
controlled drift types.

Output:

results/paired_experiment_results.csv
"""

import csv
from pathlib import Path

from data.adapters.multiwoz_adapter import (
    MultiWOZAdapter
)

from experiments.experiment_runner import (
    ExperimentRunner
)

from drift_injection.drift_types import (
    DriftType
)


class BatchExperimentRunner:

    def __init__(self, dataset_path):

        self.adapter = MultiWOZAdapter(
            dataset_path
        )

        self.runner = ExperimentRunner()

    # =====================================================

    def run(

        self,

        num_dialogues=10,

        drift_types=None,

        output_file=(
            "results/"
            "paired_experiment_results.csv"
        )

    ):

        Path("results").mkdir(
            exist_ok=True
        )

        if drift_types is None:

            drift_types = [

                DriftType.SLOT_UPDATE,

                DriftType.SLOT_INSERTION,

                DriftType.SLOT_DELETION,

                DriftType.CONTRADICTION,

                DriftType.GOAL_DRIFT,

                DriftType.MULTI_SLOT

            ]

        dialogue_ids = (
            self.adapter
            .list_dialogue_ids()
            [:num_dialogues]
        )

        results = []

        total = (
            len(dialogue_ids)
            * len(drift_types)
        )

        experiment_number = 0

        # =================================================
        # Conversations
        # =================================================

        for dialogue_id in dialogue_ids:

            print()
            print("=" * 60)
            print(
                f"Conversation: {dialogue_id}"
            )
            print("=" * 60)

            conversation = (
                self.adapter
                .to_conversation(
                    dialogue_id
                )
            )

            belief_index = (
                self._find_first_valid_belief(
                    conversation
                )
            )

            if belief_index is None:

                print(
                    "Skipped: no valid belief."
                )

                continue

            # =============================================
            # Drift types
            # =============================================

            for drift_type in drift_types:

                experiment_number += 1

                print(
                    f"[{experiment_number}/{total}] "
                    f"{drift_type}"
                )

                try:

                    # -------------------------------------
                    # Run paired experiment
                    # -------------------------------------

                    result = self.runner.run(

                        conversation,

                        belief_index,

                        drift_type

                    )

                    baseline = result[
                        "baseline"
                    ]

                    proposed = result[
                        "proposed"
                    ]

                    results.append(
                        baseline
                    )

                    results.append(
                        proposed
                    )

                    print(
                        f"   Baseline BRA : "
                        f"{baseline.belief_revision_accuracy:.3f}"
                    )

                    print(
                        f"   Proposed BRA : "
                        f"{proposed.belief_revision_accuracy:.3f}"
                    )

                    print(
                        f"   Proposed ASR : "
                        f"{proposed.adaptation_success_rate:.3f}"
                    )

                except Exception as e:

                    print(
                        f"   FAILED: {e}"
                    )

        # =================================================
        # Export
        # =================================================

        self._export_csv(
            results,
            output_file
        )

        print()
        print("=" * 60)
        print("PAIRED EXPERIMENT COMPLETE")
        print("=" * 60)

        print(
            f"Result rows : {len(results)}"
        )

        print(
            f"CSV saved   : {output_file}"
        )

        return results

    # =====================================================

    def _find_first_valid_belief(
        self,
        conversation
    ):

        for i, belief in enumerate(
            conversation.belief_states
        ):

            if belief.slots:

                return i

        return None

    # =====================================================

    def _export_csv(
        self,
        results,
        filename
    ):

        fieldnames = [

            "Conversation",

            "Condition",

            "DriftType",

            "CRS",

            "BRA",

            "ASI",

            "CRR",

            "HR",

            "ASR",

            "EDS",

            "ERR",
            
            "AdaptationAction"


        ]

        with open(

            filename,

            "w",

            newline="",

            encoding="utf-8"

        ) as csvfile:

            writer = csv.DictWriter(

                csvfile,

                fieldnames=fieldnames

            )

            writer.writeheader()

            for result in results:

                writer.writerow(
                    result.to_dict()
                )