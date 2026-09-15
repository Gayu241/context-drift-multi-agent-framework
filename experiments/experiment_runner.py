"""
experiment_runner.py

Runs a paired experiment:

1. BASELINE
   Evaluates the injected drift without recovery.

2. PROPOSED
   Runs the cognitive pipeline and evaluates recovery
   at the exact belief state where drift was injected.
"""

from evaluation.experiment_preparer import (
    ExperimentPreparer
)

from evaluation.evaluation_runner import (
    EvaluationRunner
)

from pipeline.cognitive_pipeline import (
    CognitivePipeline
)

from drift_injection.drift_types import (
    DriftType
)


class ExperimentRunner:

    def __init__(self):

        self.preparer = ExperimentPreparer()

        self.pipeline = CognitivePipeline()

        self.evaluator = EvaluationRunner(
            self.pipeline
        )

    # =====================================================

    def run(
        self,
        conversation,
        belief_index,
        drift_type=DriftType.SLOT_DELETION
    ):

        # -------------------------------------------------
        # Prepare controlled experiment
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
        # BASELINE
        # -------------------------------------------------

        baseline = self.evaluator.evaluate_baseline(
            experiment,
            ground_truth,
            drifted
        )

        # -------------------------------------------------
        # PROPOSED FRAMEWORK
        # -------------------------------------------------

        proposed = self.evaluator.evaluate(
            experiment,
            ground_truth,
            drifted,
            drift_type,
            target_belief_index=belief_index
        )

        # -------------------------------------------------
        # Return paired results
        # -------------------------------------------------

        return {
            "baseline": baseline,
            "proposed": proposed,
            "ground_truth": ground_truth,
            "drifted": drifted
        }