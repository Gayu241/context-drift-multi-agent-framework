"""
equilibrium_ablation_runner.py

Ablation experiment for the proposed
Equilibrium-Based Drift Control mechanism.

Conditions:

1. STANDARD
   Existing ResearchAdaptationPolicy

2. EQUILIBRIUM
   EquilibriumAdaptationPolicy

Both conditions receive the EXACT SAME
conversation, ground truth, and injected drift.

This isolates the effect of the equilibrium
adaptation policy.
"""

import csv
from pathlib import Path

from evaluation.experiment_preparer import (
    ExperimentPreparer
)

from evaluation.evaluation_runner import (
    EvaluationRunner
)

from pipeline.cognitive_pipeline import (
    CognitivePipeline
)

from agents.response_adaptation_agent import (
    ResponseAdaptationAgent
)

from agents.equilibrium_adaptation_policy import (
    EquilibriumAdaptationPolicy
)

from drift_injection.drift_types import (
    DriftType
)

from data.adapters.multiwoz_adapter import (
    MultiWOZAdapter
)


class EquilibriumAblationRunner:

    def __init__(
        self,
        dataset_path,
        equilibrium_boundary=0.35
    ):

        self.dataset_path = dataset_path

        self.equilibrium_boundary = (
            equilibrium_boundary
        )

        self.adapter = MultiWOZAdapter(
            dataset_path
        )

        self.preparer = ExperimentPreparer()

    # =====================================================
    # STANDARD FRAMEWORK
    # =====================================================

    def run_standard(
        self,
        experiment,
        ground_truth,
        drifted,
        drift_type,
        belief_index
    ):

        pipeline = CognitivePipeline()

        evaluator = EvaluationRunner(
            pipeline
        )

        result = evaluator.evaluate(
            experiment,
            ground_truth,
            drifted,
            drift_type=drift_type,
            target_belief_index=belief_index
        )

        return result

    # =====================================================
    # EQUILIBRIUM FRAMEWORK
    # =====================================================

    def run_equilibrium(
        self,
        experiment,
        ground_truth,
        drifted,
        drift_type,
        belief_index
    ):

        policy = (
            EquilibriumAdaptationPolicy(
                equilibrium_boundary=(
                    self.equilibrium_boundary
                )
            )
        )

        pipeline = CognitivePipeline()

        pipeline.adaptation = (
            ResponseAdaptationAgent(
                policy=policy
            )
        )

        evaluator = EvaluationRunner(
            pipeline
        )

        result = evaluator.evaluate(
            experiment,
            ground_truth,
            drifted,
            drift_type=drift_type,
            target_belief_index=belief_index
        )

        return result

    # =====================================================
    # FIND VALID BELIEF
    # =====================================================

    def find_belief_index(
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
    # RUN ONE PAIRED ABLATION
    # =====================================================

    def run_one(
        self,
        conversation,
        belief_index,
        drift_type
    ):

        # -------------------------------------------------
        # Prepare controlled drift
        # -------------------------------------------------

        (
            experiment,
            ground_truth,
            drifted
        ) = self.preparer.prepare(
            conversation,
            belief_index,
            drift_type
        )

        # -------------------------------------------------
        # Preserve original belief
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
        # Standard condition
        # -------------------------------------------------

        standard = self.run_standard(
            experiment,
            ground_truth,
            drifted,
            drift_type,
            belief_index
        )

        # -------------------------------------------------
        # IMPORTANT:
        #
        # Create a fresh experiment for the
        # equilibrium condition.
        #
        # This prevents the first pipeline run
        # from modifying state used by the second.
        # -------------------------------------------------

        (
            equilibrium_experiment,
            equilibrium_ground_truth,
            equilibrium_drifted
        ) = self.preparer.prepare(
            conversation,
            belief_index,
            drift_type
        )

        if not hasattr(
            equilibrium_experiment,
            "metadata"
        ):

            equilibrium_experiment.metadata = {}

        equilibrium_experiment.metadata[
            "pre_drift_belief"
        ] = equilibrium_ground_truth

        # -------------------------------------------------
        # Equilibrium condition
        # -------------------------------------------------

        equilibrium = self.run_equilibrium(
            equilibrium_experiment,
            equilibrium_ground_truth,
            equilibrium_drifted,
            drift_type,
            belief_index
        )

        return {
            "standard": standard,
            "equilibrium": equilibrium
        }

    # =====================================================
    # BATCH
    # =====================================================

    def run(
        self,
        num_dialogues=10,
        drift_types=None,
        output_file=(
            "results/"
            "equilibrium_ablation_results.csv"
        )
    ):

        Path(
            "results"
        ).mkdir(
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

        rows = []

        total = (
            len(dialogue_ids)
            * len(drift_types)
        )

        experiment_number = 0

        # =================================================
        # CONVERSATIONS
        # =================================================

        for dialogue_id in dialogue_ids:

            print()
            print(
                "=" * 70
            )

            print(
                "Conversation:",
                dialogue_id
            )

            print(
                "=" * 70
            )

            conversation = (
                self.adapter
                .to_conversation(
                    dialogue_id
                )
            )

            belief_index = (
                self.find_belief_index(
                    conversation
                )
            )

            if belief_index is None:

                print(
                    "Skipped: no valid belief."
                )

                continue

            # =============================================
            # DRIFT TYPES
            # =============================================

            for drift_type in drift_types:

                experiment_number += 1

                print()
                print(
                    f"[{experiment_number}/{total}] "
                    f"{drift_type}"
                )

                try:

                    results = self.run_one(
                        conversation,
                        belief_index,
                        drift_type
                    )

                    standard = (
                        results["standard"]
                    )

                    equilibrium = (
                        results["equilibrium"]
                    )

                    rows.append(
                        self.result_row(
                            standard,
                            "STANDARD"
                        )
                    )

                    rows.append(
                        self.result_row(
                            equilibrium,
                            "EQUILIBRIUM"
                        )
                    )

                    print(
                        f"   Standard "
                        f"BRA : "
                        f"{standard.belief_revision_accuracy:.3f}"
                    )

                    print(
                        f"   Equilibrium "
                        f"BRA : "
                        f"{equilibrium.belief_revision_accuracy:.3f}"
                    )

                    print(
                        f"   Standard "
                        f"Action : "
                        f"{standard.adaptation_action}"
                    )

                    print(
                        f"   Equilibrium "
                        f"Action : "
                        f"{equilibrium.adaptation_action}"
                    )

                except Exception as e:

                    print(
                        f"   FAILED: {e}"
                    )

        # =================================================
        # EXPORT
        # =================================================

        self.export(
            rows,
            output_file
        )

        print()
        print(
            "=" * 70
        )

        print(
            "EQUILIBRIUM ABLATION COMPLETE"
        )

        print(
            "=" * 70
        )

        print(
            "Rows :",
            len(rows)
        )

        print(
            "CSV  :",
            output_file
        )

        return rows

    # =====================================================
    # RESULT ROW
    # =====================================================

    def result_row(
        self,
        result,
        condition
    ):

        data = result.to_dict()

        data["Condition"] = condition

        return data

    # =====================================================
    # CSV EXPORT
    # =====================================================

    def export(
        self,
        rows,
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

            for row in rows:

                writer.writerow(
                    row
                )