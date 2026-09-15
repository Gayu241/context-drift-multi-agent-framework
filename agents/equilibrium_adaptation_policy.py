"""
equilibrium_adaptation_policy.py

Equilibrium-Based Drift Control policy.

Adaptation is triggered only when the magnitude
of the equilibrium deviation exceeds the defined
equilibrium boundary.

This implements the proposed equilibrium-based
adaptation mechanism.
"""

from core.adaptation_action import AdaptationAction
from core.adaptation_report import AdaptationReport


class EquilibriumAdaptationPolicy:

    def __init__(
        self,
        equilibrium_boundary=0.35
    ):

        self.equilibrium_boundary = (
            equilibrium_boundary
        )

    # =================================================

    def decide(
        self,
        drift_report,
        validation_report,
        cognitive_state
    ):

        drift_level = (
            drift_report.drift_level
        )

        if hasattr(
            drift_level,
            "name"
        ):

            drift_level = (
                drift_level.name
            )

        equilibrium = abs(
            float(
                drift_report.equilibrium_score
            )
        )

        belief_valid = (
            validation_report.is_valid
        )

        goal_available = bool(
            cognitive_state.conversation.goal
        )

        memory_summary = (
            cognitive_state.memory.summary()
        )

        memory_available = (

            memory_summary[
                "short_term"
            ] > 0

            or

            memory_summary[
                "reflection_queue"
            ] > 0

            or

            memory_summary[
                "experience_memory"
            ] > 0

        )

        # =================================================
        # EQUILIBRIUM CONTROL
        # =================================================

        if equilibrium < self.equilibrium_boundary:

            return AdaptationReport(

                action=AdaptationAction.NONE,

                reason=(
                    "Equilibrium maintained. "
                    "Deviation remains below "
                    "adaptation boundary."
                ),

                belief_valid=belief_valid,

                goal_available=goal_available,

                memory_available=memory_available

            )

        # =================================================
        # ADAPTATION REQUIRED
        # =================================================

        if drift_level == "HIGH_DRIFT":

            if memory_available:

                return AdaptationReport(

                    action=(
                        AdaptationAction
                        .RETRIEVE_MEMORY
                    ),

                    reason=(
                        "Equilibrium boundary exceeded "
                        "during high drift. "
                        "Experience memory retrieved "
                        "for recovery."
                    ),

                    belief_valid=belief_valid,

                    goal_available=goal_available,

                    memory_available=True

                )

            return AdaptationReport(

                action=(
                    AdaptationAction
                    .REBUILD_CONTEXT
                ),

                reason=(
                    "Equilibrium boundary exceeded "
                    "and reliable memory unavailable. "
                    "Context rebuilt."
                ),

                belief_valid=belief_valid,

                goal_available=goal_available,

                memory_available=False

            )

        # =================================================
        # MODERATE DRIFT
        # =================================================

        if drift_level == "MODERATE_DRIFT":

            if not belief_valid:

                return AdaptationReport(

                    action=(
                        AdaptationAction
                        .REBUILD_CONTEXT
                    ),

                    reason=(
                        "Equilibrium boundary exceeded "
                        "with invalid belief."
                    ),

                    belief_valid=False,

                    goal_available=goal_available,

                    memory_available=memory_available

                )

            return AdaptationReport(

                action=(
                    AdaptationAction
                    .REPAIR_BELIEF
                ),

                reason=(
                    "Equilibrium boundary exceeded. "
                    "Belief repaired using current context."
                ),

                belief_valid=True,

                goal_available=goal_available,

                memory_available=memory_available

            )

        # =================================================
        # LOW DRIFT BUT ABOVE EQUILIBRIUM
        # =================================================

        if drift_level == "LOW_DRIFT":

            return AdaptationReport(

                action=(
                    AdaptationAction
                    .REMIND_GOAL
                ),

                reason=(
                    "Equilibrium boundary exceeded "
                    "despite low drift. Goal reminder "
                    "used as lightweight adaptation."
                ),

                belief_valid=belief_valid,

                goal_available=goal_available,

                memory_available=memory_available

            )

        # =================================================
        # FALLBACK
        # =================================================

        return AdaptationReport(

            action=AdaptationAction.NONE,

            reason=(
                "No adaptation required."
            ),

            belief_valid=belief_valid,

            goal_available=goal_available,

            memory_available=memory_available

        )