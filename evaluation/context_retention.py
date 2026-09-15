"""
context_retention.py

Continuous Context Retention Score (CRS).

Measures how much of the original conversational context
has been preserved after drift recovery.

The metric compares each ground-truth slot value with the
corresponding recovered value using sentence embeddings.

For each ground-truth slot:

    similarity = cosine_similarity(ground_truth, recovered)

The final CRS is the mean slot-level retention score.

CRS ∈ [0, 1]

1.0 = complete contextual retention
0.0 = no contextual retention
"""

from evaluation.embedding_model import get_embedding_model
from sklearn.metrics.pairwise import cosine_similarity

from evaluation.metrics import EvaluationMetric


class ContextRetentionScore(EvaluationMetric):

    def __init__(self):

        super().__init__("Context Retention Score")

        self.model = get_embedding_model()

    # ---------------------------------------------------------

    def _similarity(self, expected, actual):

        expected = str(expected).strip()
        actual = str(actual).strip()

        # Exact match should always receive maximum score.
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

        # Convert [-1, 1] to [0, 1]
        score = (cosine + 1.0) / 2.0

        return float(max(0.0, min(1.0, score)))

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

            # Empty / missing semantic values
            if actual in ("", None, "not mentioned"):

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

    def lost_context(
        self,
        ground_truth,
        recovered
    ):

        gt = ground_truth.slots
        rb = recovered.slots

        lost = {}

        for slot, expected in gt.items():

            if slot not in rb:

                lost[slot] = expected

                continue

            actual = rb[slot]

            if actual in ("", None, "not mentioned"):

                lost[slot] = {
                    "expected": expected,
                    "actual": actual
                }

                continue

            similarity = self._similarity(
                expected,
                actual
            )

            if similarity < 1.0:

                lost[slot] = {
                    "expected": expected,
                    "actual": actual,
                    "similarity": similarity
                }

        return lost

    # ---------------------------------------------------------

    def retained_context(
        self,
        ground_truth,
        recovered
    ):

        gt = ground_truth.slots
        rb = recovered.slots

        retained = {}

        for slot, expected in gt.items():

            if slot not in rb:

                continue

            actual = rb[slot]

            if actual in ("", None, "not mentioned"):

                continue

            similarity = self._similarity(
                expected,
                actual
            )

            retained[slot] = {
                "expected": expected,
                "actual": actual,
                "similarity": similarity
            }

        return retained