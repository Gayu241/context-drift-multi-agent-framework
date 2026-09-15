"""
cognitive_state_manager.py

Maintains the shared CognitiveState throughout
the execution of the cognitive pipeline.
"""

from core.cognitive_state import CognitiveState
from core.cognitive_status import CognitiveStatus
from core.memory import Memory


class CognitiveStateManager:

    """
    Maintains the lifecycle of the shared CognitiveState.
    """

    # =====================================================

    def initialize(self, conversation):

        state = CognitiveState(
            conversation=conversation
        )

        state.memory = Memory()

        state.status = CognitiveStatus.READY

        return state

    # =====================================================

    def update_belief(

        self,

        state,

        belief

    ):

        state.current_belief = belief

        state.belief_history.append(belief)

        return state

    # =====================================================

    def update_changes(

        self,

        state,

        changes

    ):

        state.context_changes = changes

        return state

    # =====================================================

    def update_drift(

        self,

        state,

        drift

    ):

        state.drift_report = drift

        state.drift_history.append(drift)

        return state

    # =====================================================

    def update_validation(

        self,

        state,

        validation

    ):

        state.validation_report = validation

        state.validation_history.append(validation)

        return state

    # =====================================================

    def finalize(

        self,

        state

    ):

        state.status = CognitiveStatus.READY

        return state