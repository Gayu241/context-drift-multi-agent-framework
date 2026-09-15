"""
embedding_model.py

Shared sentence-transformer model used by evaluation metrics.

The model is loaded once per Python process and reused by:
- Context Retention Score
- Belief Revision Accuracy
- Hallucination Rate
"""

from sentence_transformers import SentenceTransformer


_MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


def get_embedding_model():
    """
    Return the shared SentenceTransformer instance.

    The model is lazily loaded the first time this function
    is called and reused for all subsequent calls.
    """

    global _model

    if _model is None:
        print(f"Loading shared embedding model: {_MODEL_NAME}")
        _model = SentenceTransformer(_MODEL_NAME)

    return _model