"""
test_equilibrium_ablation_runner.py
"""

from experiments.equilibrium_ablation_runner import (
    EquilibriumAblationRunner
)

from drift_injection.drift_types import (
    DriftType
)


def main():

    runner = EquilibriumAblationRunner(

        "datasets/multiwoz/data/"
        "MULTIWOZ2.4/data.json",

        equilibrium_boundary=0.35

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

        ]

    )


if __name__ == "__main__":

    main()