"""
test_batch_experiment_runner.py

Runs a small batch sanity check before the
full MultiWOZ experiment.
"""

from experiments.batch_experiment_runner import (
    BatchExperimentRunner
)

from drift_injection.drift_types import (
    DriftType
)


DATASET_PATH = (
    "datasets/multiwoz/data/"
    "MULTIWOZ2.4/data.json"
)


def main():

    runner = BatchExperimentRunner(
        DATASET_PATH
    )

    runner.run(

        num_dialogues=10,

        drift_types=[

            DriftType.SLOT_UPDATE,

            DriftType.SLOT_INSERTION,

            DriftType.SLOT_DELETION,

            DriftType.CONTRADICTION,

            DriftType.GOAL_DRIFT,

            DriftType.MULTI_SLOT

        ],

        output_file=(
            "results/"
            "paired_experiment_results.csv"
        )

    )


if __name__ == "__main__":

    main()