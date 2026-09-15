"""
cognitive_pipeline.py

Runs the complete cognitive architecture over a conversation.

Supports optional target_belief_index for controlled experiments,
allowing evaluation of the exact belief state where drift was injected.
"""

import copy

from agents.context_monitoring_agent import ContextMonitoringAgent
from agents.drift_detection_agent import DriftDetectionAgent
from agents.belief_validation_agent import BeliefValidationAgent
from agents.reflective_memory_agent import ReflectiveMemoryAgent
from agents.response_adaptation_agent import ResponseAdaptationAgent

from agents.cognitive_state_manager import CognitiveStateManager


class CognitivePipeline:

    def __init__(self):

        self.state_manager = CognitiveStateManager()

        self.monitor = ContextMonitoringAgent()

        self.drift = DriftDetectionAgent()

        self.validator = BeliefValidationAgent()

        self.memory = ReflectiveMemoryAgent()

        self.adaptation = ResponseAdaptationAgent()

    # =====================================================
    # RUN PIPELINE
    # =====================================================

    def run(
        self,
        conversation,
        target_belief_index=None
    ):

        state = self.state_manager.initialize(
            conversation
        )

        # -------------------------------------------------
        # Seed historical memory for controlled experiments
        # -------------------------------------------------

        if hasattr(conversation, "metadata"):
            pre_drift_belief = (
                conversation.metadata.get(
                    "pre_drift_belief"
            )
        )
            if pre_drift_belief is not None: 
                from core.memory_record import MemoryRecord
                memory_record = MemoryRecord(
                    turn_id=pre_drift_belief.turn_id,
                    category=pre_drift_belief.domain.upper(),
                    content=copy.deepcopy(
                        pre_drift_belief.slots
                    ),
                    importance=1.0,
                    confidence=1.0,
                    source="PreDriftHistoricalContext"
                )

                state.memory.add_experience(
                    memory_record
                )

        beliefs = conversation.belief_states

        if len(beliefs) == 0:

            print(
                "\n========== LAST 10 BELIEF STATES ==========\n"
            )

            for belief in beliefs[-10:]:

                print(
                    belief.turn_id,
                    belief.domain,
                    belief.slots
                )

            return self.state_manager.finalize(
                state
            )

        # =================================================
        # Target experiment tracking
        # =================================================

        target_belief = None
        target_drift = None
        target_validation = None
        target_changes = None
        target_adaptation = None

        # =================================================
        # First belief
        # =================================================

        previous = beliefs[0]

        state = self.state_manager.update_belief(
            state,
            previous
        )

        validation = self.validator.validate(
            previous
        )

        state = self.state_manager.update_validation(
            state,
            validation
        )

        empty_changes = []

        drift_report = self.drift.detect(
            empty_changes,
            len(previous.slots)
        )

        state = self.state_manager.update_drift(
            state,
            drift_report
        )

        state = self.memory.process(
            state
        )

        state = self.adaptation.process(
            state
        )

        # -------------------------------------------------
        # Capture first belief if it is the target
        # -------------------------------------------------

        if target_belief_index == 0:

            target_belief = copy.deepcopy(
                state.current_belief
            )

            target_drift = copy.deepcopy(
                state.drift_report
            )

            target_validation = copy.deepcopy(
                state.validation_report
            )

            target_changes = copy.deepcopy(
                state.context_changes
            )

            target_adaptation = copy.deepcopy(
                state.adaptation_report
            )

        # =================================================
        # Remaining beliefs
        # =================================================

        for index, current in enumerate(
            beliefs[1:],
            start=1
        ):

            # -------------------------------------------------
            # Ignore empty beliefs EXCEPT when the empty belief
            # is the exact target of the experiment.
            # -------------------------------------------------

            if (
                not current.slots
                and not current.booking
                and index != target_belief_index
            ):

                continue

            # -------------------------------------------------
            # Update current belief
            # -------------------------------------------------

            state = self.state_manager.update_belief(
                state,
                current
            )

            # -------------------------------------------------
            # Monitor contextual changes
            # -------------------------------------------------

            changes = self.monitor.monitor(
                previous,
                current
            )

            state = self.state_manager.update_changes(
                state,
                changes
            )

            # -------------------------------------------------
            # Calculate comparison slot count
            # -------------------------------------------------

            total_slots = len(
                set(previous.slots.keys())
                |
                set(current.slots.keys())
            )

            # -------------------------------------------------
            # Drift detection
            # -------------------------------------------------

            drift = self.drift.detect(
                changes,
                total_slots
            )

            state = self.state_manager.update_drift(
                state,
                drift
            )

            # -------------------------------------------------
            # Validation
            # -------------------------------------------------

            validation = self.validator.validate(
                current
            )

            state = self.state_manager.update_validation(
                state,
                validation
            )

            # -------------------------------------------------
            # Memory
            # -------------------------------------------------

            state = self.memory.process(
                state
            )

            # -------------------------------------------------
            # Adaptation
            # -------------------------------------------------

            state = self.adaptation.process(
                state
            )

            # =================================================
            # Capture target state AFTER adaptation
            # =================================================

            if index == target_belief_index:

                target_belief = copy.deepcopy(
                    state.current_belief
                )

                target_drift = copy.deepcopy(
                    state.drift_report
                )

                target_validation = copy.deepcopy(
                    state.validation_report
                )

                target_changes = copy.deepcopy(
                    state.context_changes
                )

                target_adaptation = copy.deepcopy(
                    state.adaptation_report
                )

            # -------------------------------------------------
            # IMPORTANT:
            # Keep previous meaningful belief.
            # -------------------------------------------------

            previous = current

        # =====================================================
        # Restore target state for controlled evaluation
        # =====================================================

        if (
            target_belief_index is not None
            and target_belief is not None
        ):

            state.current_belief = target_belief

            state.drift_report = target_drift

            state.validation_report = target_validation

            state.context_changes = target_changes

            state.adaptation_report = target_adaptation

        # =====================================================
        # Finalize
        # =====================================================

        return self.state_manager.finalize(
            state
        )

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self, state):

        print()

        print("=" * 50)

        print(
            "COGNITIVE PIPELINE SUMMARY"
        )

        print("=" * 50)

        print(
            "Conversation :",
            state.conversation.conversation_id
        )

        print(
            "Dataset      :",
            state.conversation.dataset
        )

        print(
            "Beliefs      :",
            len(
                state.conversation.belief_states
            )
        )

        print(
            "Changes      :",
            len(state.context_changes)
        )

        print(
            "Memory       :",
            state.memory.summary()
        )

        print(
            "Status       :",
            state.status.value
        )

        if state.drift_report:

            print(
                "Drift Level  :",
                state.drift_report.drift_level
            )

        if state.validation_report:

            print(
                "Valid Belief :",
                state.validation_report.is_valid
            )

        if hasattr(
            state,
            "adaptation_report"
        ):

            print(
                "Adaptation   :",
                state.adaptation_report.action.value
            )

        print(
            "=" * 50
        )

        print()