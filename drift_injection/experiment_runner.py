"""
experiment_runner.py

Runs large-scale drift injection experiments over MultiWOZ
and evaluates the complete Context Drift Detection Framework.
"""

import random

from evaluation.evaluation_runner import EvaluationRunner

from drift_injection.drift_injector import DriftInjector
from drift_injection.drift_scenarios import SCENARIOS


class ExperimentRunner:

    def __init__(

        self,

        adapter,

        pipeline,

        exporter

    ):

        self.adapter = adapter

        self.pipeline = pipeline

        self.exporter = exporter

        self.injector = DriftInjector()

        self.evaluator = EvaluationRunner(
            pipeline
        )

    # ======================================================

    def run(

        self,

        conversations=100,

        scenario="Scenario 1"

    ):

        print()

        print("=" * 80)
        print("RUNNING EXPERIMENT")
        print("=" * 80)

        results = []

        ids = self.adapter.list_dialogue_ids()

        random.shuffle(ids)

        ids = ids[:conversations]

        drift_types = SCENARIOS[scenario]

        for i, dialogue_id in enumerate(ids, start=1):

            conversation = self.adapter.to_conversation(
                dialogue_id
            )

            # ---------------------------------------------
            # Inject Drift
            # ---------------------------------------------

            for belief in conversation.belief_states:

                for drift in drift_types:

                    injected = self.injector.inject(
                        belief,
                        drift
                    )

                    belief.slots = injected.slots

            # ---------------------------------------------
            # Evaluate
            # ---------------------------------------------

            result = self.evaluator.evaluate(
                conversation
            )

            results.append(result)

            print(

                f"[{i}/{conversations}]",

                conversation.conversation_id,

                "Completed"

            )

        # ---------------------------------------------
        # Export CSV
        # ---------------------------------------------

        self.exporter.export(results)

        print()

        print("=" * 80)
        print("EXPERIMENT FINISHED")
        print("=" * 80)

        return results