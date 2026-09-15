"""
export_results.py

Exports evaluation results to CSV.
"""

import csv
from pathlib import Path


class EvaluationExporter:

    def export(

        self,

        results,

        output_path="results/evaluation_results.csv"

    ):

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.DictWriter(

                csvfile,

                fieldnames=[

                    "conversation_id",

                    "CRS",

                    "BRA",

                    "ASI",

                    "CRR",

                    "HR",

                    "ASR"

                ]

            )

            writer.writeheader()

            for result in results:

                writer.writerow(
                    result.to_dict()
                )

        print()

        print(f"Results exported to {output_path}")