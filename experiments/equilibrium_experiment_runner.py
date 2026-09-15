"""
equilibrium_experiment_runner.py

Compares the existing drift-level adaptation policy
with the proposed Equilibrium-Based Drift Control policy.

Conditions:

1. STANDARD
   Existing ResearchAdaptationPolicy

2. EQUILIBRIUM
   EquilibriumAdaptationPolicy

The purpose is to isolate the contribution of
equilibrium-based adaptation control.
"""

from agents.response_adaptation_agent import (
    ResponseAdaptationAgent
)

from agents.equilibrium_adaptation_policy import (
    EquilibriumAdaptationPolicy
)

from pipeline.cognitive_pipeline import (
    CognitivePipeline
)

from evaluation.evaluation_runner import (
    EvaluationRunner
)


class EquilibriumExperimentRunner:

    def __init__(
        self,
        equilibrium_boundary=0.35
    ):

        self.equilibrium_boundary = (
            equilibrium_boundary
        )

    # =================================================
    # STANDARD FRAMEWORK
    # =================================================

    def run_standard(
        self,
        conversation,
        ground_truth,
        drifted_belief,
        drift_type,
        target_belief_index
    ):

        pipeline = CognitivePipeline()

        evaluator = EvaluationRunner(
            pipeline
        )

        return evaluator.evaluate(
            conversation,
            ground_truth,
            drifted_belief,
            drift_type=drift_type,
            target_belief_index=target_belief_index
        )

    # =================================================
    # EQUILIBRIUM FRAMEWORK
    # =================================================

    def run_equilibrium(
        self,
        conversation,
        ground_truth,
        drifted_belief,
        drift_type,
        target_belief_index
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

        return evaluator.evaluate(
            conversation,
            ground_truth,
            drifted_belief,
            drift_type=drift_type,
            target_belief_index=target_belief_index
        )

    # =================================================
    # PAIRED RUN
    # =================================================

    def run(
        self,
        conversation,
        ground_truth,
        drifted_belief,
        drift_type,
        target_belief_index
    ):

        standard = self.run_standard(
            conversation,
            ground_truth,
            drifted_belief,
            drift_type,
            target_belief_index
        )

        equilibrium = self.run_equilibrium(
            conversation,
            ground_truth,
            drifted_belief,
            drift_type,
            target_belief_index
        )

        return {
            "standard": standard,
            "equilibrium": equilibrium
        }