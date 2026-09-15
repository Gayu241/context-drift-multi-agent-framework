"""
belief_revision_accuracy.py

Continuous Belief Revision Accuracy (BRA).

Measures how accurately the framework restores the
original belief state after context drift.

Unlike a binary exact-match metric, BRA uses
vector-space similarity between corresponding
ground-truth and recovered slot values.

BRA ∈ [0, 1]

1.0 = complete belief recovery
0.0 = complete belief loss
"""

from evaluation.embedding_model import get_embedding_model
from sklearn.metrics.pairwise import cosine_similarity

from evaluation.metrics import EvaluationMetric


class BeliefRevisionAccuracy(EvaluationMetric):

    def __init__(self):

        super().__init__(
            "Belief Revision Accuracy"
        )

        self.model = get_embedding_model()

    # ---------------------------------------------------------

    def _similarity(self, expected, actual):

        expected = str(expected).strip()
        actual = str(actual).strip()

        if expected.lower() == actual.lower():

            return 1.0

        embeddings = self.model.encode(
            [expected, actual],
            normalize_embeddings=True
        )

        cosine = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        score = (cosine + 1.0) / 2.0

        return float(
            max(0.0, min(1.0, score))
        )

    # ---------------------------------------------------------

    def evaluate(
        self,
        ground_truth,
        recovered
    ) -> float:

        gt = ground_truth.slots
        rb = recovered.slots

        if not gt:

            return 1.0

        scores = []

        for slot, expected in gt.items():

            if slot not in rb:

                scores.append(0.0)

                continue

            actual = rb[slot]

            if actual in (
                "",
                None,
                "not mentioned"
            ):

                scores.append(0.0)

                continue

            scores.append(
                self._similarity(
                    expected,
                    actual
                )
            )

        if not scores:

            return 0.0

        return sum(scores) / len(scores)

    # ---------------------------------------------------------

    def detailed_report(
        self,
        ground_truth,
        recovered
    ):

        gt = ground_truth.slots
        rb = recovered.slots

        report = []

        for slot, expected in gt.items():

            actual = rb.get(slot)

            if actual in (
                None,
                "",
                "not mentioned"
            ):

                similarity = 0.0

            else:

                similarity = self._similarity(
                    expected,
                    actual
                )

            report.append({

                "slot": slot,

                "expected": expected,

                "actual": actual,

                "similarity": similarity,

                "correct": (
                    expected == actual
                )

            })

        return report