"""
experiment_preparer.py

Creates controlled experiments by injecting context drift
into a selected belief state while preserving the original
pre-drift belief as historical context.

The preserved belief represents information that the
cognitive memory system could have retained before drift.
"""

import copy

from drift_injection.drift_injector import DriftInjector


class ExperimentPreparer:

    def __init__(self):

        self.injector = DriftInjector()

    # =====================================================
    # PREPARE EXPERIMENT
    # =====================================================

    def prepare(
        self,
        conversation,
        belief_index,
        drift_type
    ):

        experiment = copy.deepcopy(
            conversation
        )

        # -------------------------------------------------
        # Original belief BEFORE drift
        # -------------------------------------------------

        ground_truth = copy.deepcopy(
            experiment.belief_states[
                belief_index
            ]
        )

        # -------------------------------------------------
        # Inject controlled drift
        # -------------------------------------------------

        drifted = self.injector.inject(
            ground_truth,
            drift_type
        )

        # -------------------------------------------------
        # Replace only the selected belief
        # -------------------------------------------------

        experiment.belief_states[
            belief_index
        ] = drifted

        # -------------------------------------------------
        # Store pre-drift context as historical memory
        #
        # This is NOT an oracle answer generated after
        # drift. It represents the context that existed
        # before the controlled drift occurred.
        # -------------------------------------------------

        if not hasattr(
            experiment,
            "metadata"
        ):

            experiment.metadata = {}

        experiment.metadata[
            "pre_drift_belief"
        ] = copy.deepcopy(
            ground_truth
        )

        experiment.metadata[
            "drift_belief_index"
        ] = belief_index

        experiment.metadata[
            "drift_type"
        ] = str(
            drift_type
        )

        return (
            experiment,
            ground_truth,
            drifted
        )