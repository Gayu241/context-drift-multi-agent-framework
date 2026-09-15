from abc import ABC, abstractmethod

from core.adaptation_action import AdaptationAction
from core.adaptation_report import AdaptationReport


class AdaptationPolicy(ABC):

    @abstractmethod
    def decide(
        self,
        drift_report,
        validation_report,
        cognitive_state
    ) -> AdaptationReport:
        pass


class ResearchAdaptationPolicy(AdaptationPolicy):

    def decide(
        self,
        drift_report,
        validation_report,
        cognitive_state
    ) -> AdaptationReport:

        drift_level = drift_report.drift_level

        # Handle both Enum and string drift levels
        if hasattr(drift_level, "name"):
            drift_level = drift_level.name

        belief_valid = validation_report.is_valid

        goal_available = bool(
            cognitive_state.conversation.goal
        )

        memory_summary = cognitive_state.memory.summary()

        memory_available = (
            memory_summary["short_term"] > 0
            or memory_summary["reflection_queue"] > 0
            or memory_summary["experience_memory"] > 0
        )

        # -------------------------------------------------
        # NO DRIFT
        # -------------------------------------------------

        if drift_level == "NO_DRIFT":

            return AdaptationReport(
                action=AdaptationAction.NONE,
                reason="Conversation remains stable.",
                belief_valid=belief_valid,
                goal_available=goal_available,
                memory_available=memory_available
            )

        # -------------------------------------------------
        # LOW DRIFT
        # -------------------------------------------------

        if drift_level == "LOW_DRIFT":

            return AdaptationReport(
                action=AdaptationAction.REMIND_GOAL,
                reason="Minor deviation detected. Goal reminder injected.",
                belief_valid=belief_valid,
                goal_available=goal_available,
                memory_available=memory_available
            )

        # -------------------------------------------------
        # MODERATE DRIFT
        # -------------------------------------------------

        if drift_level == "MODERATE_DRIFT":

            if not belief_valid:

                return AdaptationReport(
                    action=AdaptationAction.REBUILD_CONTEXT,
                    reason="Belief invalid during moderate drift.",
                    belief_valid=False,
                    goal_available=goal_available,
                    memory_available=memory_available
                )

            return AdaptationReport(
                action=AdaptationAction.REPAIR_BELIEF,
                reason="Belief repaired using current context.",
                belief_valid=True,
                goal_available=goal_available,
                memory_available=memory_available
            )

        # -------------------------------------------------
        # HIGH DRIFT
        # -------------------------------------------------

        if drift_level == "HIGH_DRIFT":

            if memory_available:

                return AdaptationReport(
                    action=AdaptationAction.RETRIEVE_MEMORY,
                    reason="Experience memory retrieved for recovery.",
                    belief_valid=belief_valid,
                    goal_available=goal_available,
                    memory_available=True
                )

            return AdaptationReport(
                action=AdaptationAction.REBUILD_CONTEXT,
                reason="No reliable memory available. Context rebuilt.",
                belief_valid=belief_valid,
                goal_available=goal_available,
                memory_available=False
            )

        # -------------------------------------------------
        # FALLBACK
        # -------------------------------------------------

        return AdaptationReport(
            action=AdaptationAction.NONE,
            reason=f"Unknown drift level: {drift_level}",
            belief_valid=belief_valid,
            goal_available=goal_available,
            memory_available=memory_available
        )