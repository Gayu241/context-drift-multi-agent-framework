"""
evaluation_runner.py

Research Evaluation Runner

Evaluates:

1. BASELINE
   Drifted belief without recovery.

2. PROPOSED
   Full cognitive pipeline with memory-based recovery.

The proposed condition also evaluates equilibrium
before and after adaptation.
"""

import copy

from evaluation.context_retention import ContextRetentionScore
from evaluation.belief_revision_accuracy import (
    BeliefRevisionAccuracy
)
from evaluation.agent_stability import AgentStabilityIndex
from evaluation.contradiction_resolution import (
    ContradictionResolutionRate
)
from evaluation.hallucination_rate import HallucinationRate
from evaluation.adaptation_success import (
    AdaptationSuccessRate
)
from evaluation.equilibrium_deviation import (
    EquilibriumDeviationScore
)
from evaluation.equilibrium_recovery import (
    EquilibriumRecoveryRate
)

from evaluation.evaluation_result import (
    EvaluationResult
)

from agents.drift_detection_agent import (
    DriftDetectionAgent
)

from agents.context_monitoring_agent import (
    ContextMonitoringAgent
)


class EvaluationRunner:

    def __init__(self, pipeline):

        self.pipeline = pipeline

        self.crs = ContextRetentionScore()

        self.bra = BeliefRevisionAccuracy()

        self.asi = AgentStabilityIndex()

        self.crr = ContradictionResolutionRate()

        self.hr = HallucinationRate()

        self.asr = AdaptationSuccessRate()

        self.eds = EquilibriumDeviationScore()

        self.err = EquilibriumRecoveryRate()

        # ---------------------------------------------
        # Separate monitoring tools used only for
        # post-adaptation evaluation.
        # ---------------------------------------------

        self.post_monitor = (
            ContextMonitoringAgent()
        )

        self.post_drift = (
            DriftDetectionAgent()
        )

    # =====================================================
    # BASELINE
    # =====================================================

    def evaluate_baseline(
        self,
        conversation,
        ground_truth,
        drifted_belief
    ):

        """
        Evaluate the drifted conversation WITHOUT
        running the cognitive recovery pipeline.

        This establishes the no-adaptation baseline.
        """

        bra = self.bra.evaluate(
            ground_truth,
            drifted_belief
        )

        crs = self.crs.evaluate(
            ground_truth,
            drifted_belief
        )

        hr = self.hr.evaluate(
            ground_truth,
            drifted_belief
        )

        # No adaptation occurs in baseline.
        asr = 0.0

        # No pipeline history exists for baseline.
        asi = 0.0

        crr = 0.0

        # Equilibrium metrics are not evaluated
        # for the baseline condition.
        eds = 0.0
        err = 0.0
        

        return EvaluationResult(

            conversation_id=(
                conversation.conversation_id
            ),

            condition="BASELINE",

            drift_type="",

            context_retention_score=crs,

            belief_revision_accuracy=bra,

            agent_stability_index=asi,

            contradiction_resolution_rate=crr,

            hallucination_rate=hr,

            adaptation_success_rate=asr,

            equilibrium_deviation_score=eds,
            
            adaptation_action="NONE",

            equilibrium_recovery_rate=err

        )

    # =====================================================
    # PROPOSED FRAMEWORK
    # =====================================================

    def evaluate(
        self,
        conversation,
        ground_truth,
        drifted_belief,
        drift_type="",
        target_belief_index=None
    ):

        """
        Run the complete cognitive framework and
        evaluate the recovered belief.

        Equilibrium is evaluated before and after
        adaptation.
        """

        # Preserve the original drifted state before the
        # cognitive pipeline modifies the experiment in-place.
        drifted_before = copy.deepcopy(
            drifted_belief
        )

        # -------------------------------------------------
        # Run Cognitive Pipeline
        # -------------------------------------------------

        state = self.pipeline.run(
            conversation,
            target_belief_index=target_belief_index
        )

        recovered = state.current_belief

        print()
        print(
            "========== BELIEF RECOVERY DEBUG =========="
        )

        print(
            "GROUND TRUTH :",
            ground_truth.slots
        )

        print(
            "DRIFTED      :",
            drifted_before.slots
        )

        print(
            "RECOVERED    :",
            recovered.slots
            if recovered
            else None
        )

        print(
            "============================================"
        )

        # =================================================
        # BEFORE ADAPTATION
        # =================================================

        bra_before = self.bra.evaluate(
            ground_truth,
            drifted_before
        )

        # -------------------------------------------------
        # Existing drift report represents the state
        # immediately before recovery.
        # -------------------------------------------------

        drift_report = state.drift_report

        equilibrium_before = (
            drift_report.equilibrium_score
        )

        weighted_drift_before = (
            drift_report.weighted_drift_score
        )

        # =================================================
        # AFTER ADAPTATION
        # =================================================

        bra_after = self.bra.evaluate(
            ground_truth,
            recovered
        )

        crs = self.crs.evaluate(
            ground_truth,
            recovered
        )

        hr = self.hr.evaluate(
            ground_truth,
            recovered
        )

        # -------------------------------------------------
        # Adaptation Success
        # -------------------------------------------------

        asr = self.asr.evaluate(
            bra_before,
            bra_after
        )

        # =================================================
        # POST-ADAPTATION DRIFT
        # =================================================

        post_changes = []

        if recovered is not None:

            try:

                post_changes = (
                    self.post_monitor.monitor(
                        recovered,
                        ground_truth
                    )
                )

            except Exception:

                post_changes = []

        # -------------------------------------------------
        # Calculate post-adaptation drift using a separate
        # detector so the main pipeline detector state
        # is not corrupted.
        # -------------------------------------------------

        post_total_slots = len(
            set(
                recovered.slots.keys()
                if recovered
                else []
            )
            |
            set(
                ground_truth.slots.keys()
            )
        )

        post_drift_report = (
            self.post_drift.detect(
                post_changes,
                post_total_slots
            )
        )

        weighted_drift_after = (
            post_drift_report.weighted_drift_score
        )

        # =================================================
        # POST-ADAPTATION EQUILIBRIUM
        # =================================================

        # Use the same equilibrium formulation:
        #
        # E_t = alpha * D_t
        #       + beta * (D_t - D_(t-1))
        #
        # Here:
        #
        # D_t     = post-adaptation drift
        # D_(t-1) = pre-adaptation drift

        alpha = self.eds.alpha
        beta = self.eds.beta

        equilibrium_after = (

            alpha * weighted_drift_after

            + beta * (
                weighted_drift_after
                - weighted_drift_before
            )

        )

        # =================================================
        # EQUILIBRIUM DEVIATION
        # =================================================

        eds = equilibrium_before

        # =================================================
        # EQUILIBRIUM RECOVERY
        # =================================================

        err = self.err.evaluate(
            equilibrium_before,
            equilibrium_after
        )

        # =================================================
        # STABILITY
        # =================================================

        asi = self.asi.evaluate(
            state.drift_history
        )

        # =================================================
        # CONTRADICTION RESOLUTION
        # =================================================

        # Until the dedicated contradiction detector
        # is implemented, this remains explicitly
        # unavailable rather than claiming resolution.

        crr = 0.0

        # =================================================
        # DEBUG EQUILIBRIUM
        # =================================================

        print()
        print(
            "========== EQUILIBRIUM DEBUG =========="
        )

        print(
            "Weighted Drift Before :",
            round(
                weighted_drift_before,
                6
            )
        )

        print(
            "Equilibrium Before    :",
            round(
                equilibrium_before,
                6
            )
        )

        print(
            "Weighted Drift After  :",
            round(
                weighted_drift_after,
                6
            )
        )

        print(
            "Equilibrium After     :",
            round(
                equilibrium_after,
                6
            )
        )

        print(
            "ERR                   :",
            round(
                err,
                6
            )
        )

        print(
            "========================================"
        )

        # =================================================
        # RESULT
        # =================================================

        return EvaluationResult(

            conversation_id=(
                conversation.conversation_id
            ),

            condition="PROPOSED",

            drift_type=str(
                drift_type
            ),

            context_retention_score=crs,

            belief_revision_accuracy=bra_after,

            agent_stability_index=asi,

            contradiction_resolution_rate=crr,

            hallucination_rate=hr,

            adaptation_success_rate=asr,

            equilibrium_deviation_score=eds,

            equilibrium_recovery_rate=err,
            adaptation_action=(
                state.adaptation_report.action.value
                if state.adaptation_report
                else ""
            ),

        )