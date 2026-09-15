"""
hallucination_rate.py

Continuous Hallucination Rate (HR).

Measures the proportion and severity of recovered
belief information that is unsupported by the
ground-truth belief state.

New slots are treated as fully unsupported.

Existing slots with incorrect values receive a
continuous hallucination score based on semantic
distance.

HR ∈ [0, 1]

0.0 = no hallucinated information
1.0 = completely unsupported recovered information
"""

from evaluation.embedding_model import get_embedding_model
from sklearn.metrics.pairwise import cosine_similarity

from evaluation.metrics import EvaluationMetric


class HallucinationRate(EvaluationMetric):

    def __init__(self):

        super().__init__(
            "Hallucination Rate"
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

        if not rb:

            return 0.0

        hallucination_scores = []

        for slot, actual in rb.items():

            # ---------------------------------------------
            # Completely new slot
            # ---------------------------------------------

            if slot not in gt:

                hallucination_scores.append(1.0)

                continue

            expected = gt[slot]

            # ---------------------------------------------
            # Empty recovered value
            # ---------------------------------------------

            if actual in (
                "",
                None,
                "not mentioned"
            ):

                hallucination_scores.append(0.0)

                continue

            # ---------------------------------------------
            # Existing slot
            # ---------------------------------------------

            similarity = self._similarity(
                expected,
                actual
            )

            hallucination = 1.0 - similarity

            hallucination_scores.append(
                hallucination
            )

        if not hallucination_scores:

            return 0.0

        return (
            sum(hallucination_scores)
            / len(hallucination_scores)
        )

    # ---------------------------------------------------------

    def hallucinated_slots(
        self,
        ground_truth,
        recovered
    ):

        gt = ground_truth.slots
        rb = recovered.slots

        report = {}

        for slot, actual in rb.items():

            # ---------------------------------------------
            # New slot
            # ---------------------------------------------

            if slot not in gt:

                report[slot] = {

                    "type": "NEW_SLOT",

                    "value": actual,

                    "hallucination_score": 1.0

                }

                continue

            expected = gt[slot]

            # ---------------------------------------------
            # Empty value
            # ---------------------------------------------

            if actual in (
                "",
                None,
                "not mentioned"
            ):

                continue

            similarity = self._similarity(
                expected,
                actual
            )

            hallucination = 1.0 - similarity

            if hallucination > 0.0:

                report[slot] = {

                    "type": "WRONG_VALUE",

                    "expected": expected,

                    "actual": actual,

                    "similarity": similarity,

                    "hallucination_score": hallucination

                }

        return report