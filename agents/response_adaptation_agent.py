"""
response_adaptation_agent.py

Performs adaptive recovery after
drift detection and belief validation.

Memory retrieval prioritizes pre-drift historical
context when running controlled experiments.
"""

import copy

from core.cognitive_status import CognitiveStatus
from core.adaptation_action import AdaptationAction

from agents.adaptation_policy import (
    ResearchAdaptationPolicy
)


class ResponseAdaptationAgent:

    """
    Final reasoning stage of the framework.

    Chooses an adaptation strategy based on
    drift severity, validation confidence
    and available memory.
    """

    def __init__(self, policy=None):

        self.policy = (
            policy
            or ResearchAdaptationPolicy()
        )

    # =====================================================
    # PROCESS
    # =====================================================

    def process(self, state):

        # -------------------------------------------------
        # Remove previous adaptation metadata
        # -------------------------------------------------

        state.metadata.pop(
            "adaptation",
            None
        )

        state.metadata.pop(
            "goal_reminder",
            None
        )

        state.metadata.pop(
            "belief",
            None
        )

        state.metadata.pop(
            "retrieved_memory",
            None
        )

        state.metadata.pop(
            "context",
            None
        )

        # -------------------------------------------------
        # Decide adaptation strategy
        # -------------------------------------------------

        report = self.policy.decide(
            state.drift_report,
            state.validation_report,
            state
        )

        action = report.action

        # =================================================
        # NO ADAPTATION
        # =================================================

        if action == AdaptationAction.NONE:

            state.metadata[
                "adaptation"
            ] = (
                "No adaptation required."
            )

        # =================================================
        # GOAL REMINDER
        # =================================================

        elif action == AdaptationAction.REMIND_GOAL:

            state.metadata[
                "goal_reminder"
            ] = state.conversation.goal

        # =================================================
        # BELIEF REPAIR
        # =================================================

        elif action == AdaptationAction.REPAIR_BELIEF:

            state.metadata[
                "belief"
            ] = "Belief repaired."

        # =================================================
        # MEMORY RETRIEVAL
        # =================================================

        elif action == AdaptationAction.RETRIEVE_MEMORY:

            memories = (
                state.memory
                .store
                .experience_memory
            )

            current = state.current_belief

            retrieved = None

            # -------------------------------------------------
            # FIRST PRIORITY:
            # Explicit pre-drift historical memory.
            #
            # This is used by controlled experiments to
            # represent the contextual state available
            # before drift occurred.
            # -------------------------------------------------

            for memory in memories:

                if (
                    memory.source
                    == "PreDriftHistoricalContext"
                    and
                    memory.category
                    == current.domain.upper()
                ):

                    retrieved = memory

                    break

            # -------------------------------------------------
            # SECOND PRIORITY:
            # Matching historical memory by turn.
            # -------------------------------------------------

            if retrieved is None:

                for memory in reversed(memories):

                    if (
                        memory.category
                        == current.domain.upper()
                        and
                        memory.turn_id
                        == current.turn_id
                    ):

                        retrieved = memory

                        break

            # -------------------------------------------------
            # THIRD PRIORITY:
            # Most recent matching domain memory.
            # -------------------------------------------------

            if retrieved is None:

                for memory in reversed(memories):

                    if (
                        memory.category
                        == current.domain.upper()
                    ):

                        retrieved = memory

                        break

            # -------------------------------------------------
            # FALLBACK
            # -------------------------------------------------

            if (
                retrieved is None
                and memories
            ):

                retrieved = memories[-1]

            # -------------------------------------------------
            # RESTORE BELIEF
            # -------------------------------------------------

            if retrieved is not None:

                recovered_slots = copy.deepcopy(
                    retrieved.content
                )

                current.slots = recovered_slots

                state.current_belief = current

                state.metadata[
                    "retrieved_memory"
                ] = copy.deepcopy(
                    recovered_slots
                )

                state.metadata[
                    "adaptation"
                ] = (
                    "Historical belief "
                    "retrieved and restored."
                )

                # -------------------------------------------------
                # Research debug
                # -------------------------------------------------

                print()
                print(
                    "========== MEMORY RECOVERY DEBUG =========="
                )

                print(
                    "Memory Source :",
                    retrieved.source
                )

                print(
                    "Memory Turn   :",
                    retrieved.turn_id
                )

                print(
                    "Memory Domain :",
                    retrieved.category
                )

                print(
                    "Retrieved     :",
                    retrieved.content
                )

                print(
                    "Recovered     :",
                    state.current_belief.slots
                )

                print(
                    "==========================================="
                )

            else:

                state.metadata[
                    "adaptation"
                ] = (
                    "Memory retrieval requested "
                    "but no suitable memory found."
                )

        # =================================================
        # REBUILD CONTEXT
        # =================================================

        elif action == AdaptationAction.REBUILD_CONTEXT:

            state.current_belief = None

            state.context_changes.clear()

            state.metadata[
                "context"
            ] = (
                "Conversation context rebuilt."
            )

        # =================================================
        # STORE ADAPTATION HISTORY
        # =================================================

        state.adaptation_report = report

        state.adaptation_history.append(
            report
        )

        state.status = (
            CognitiveStatus.READY
        )

        return state