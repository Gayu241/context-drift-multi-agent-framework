"""
metrics.py

Abstract base class for all evaluation metrics.
"""

from abc import ABC, abstractmethod


class EvaluationMetric(ABC):
    """
    Base class for all evaluation metrics.
    """

    def __init__(self, name: str):

        self.name = name

    @abstractmethod
    def evaluate(self, *args, **kwargs):
        """
        Compute the metric.
        """
        pass

    def __str__(self):

        return self.name