"""
drift_report.py
Represents the output produced by the Drift Detection Agent
"""

from dataclasses import dataclass, field
from typing import List
from core.context_change import ContextChange


@dataclass
class DriftReport: 
    """
    Represents the detected drift for a single conversational step. 
    """
    turn_id: int
    drift_score: float 
    weighted_drift_score: float 
    equilibrium_score: float 
    drift_level: str
    context_changes: List[ContextChange] = field(default_factory=list)

    def __str__(self):
        return (
            f"\n"
            f"Turn: {self.turn_id}\n"
            f"Drift Score: {self.drift_score:.3f}\n"
            f"Weighted Drift Score: {self.weighted_drift_score:.3f}\n"
            f"Equilibrium Score: {self.equilibrium_score:.3f}\n"
            f"Drift Level: {self.drift_level}\n"
            f"Number of Changes: {len(self.context_changes)}"
            
        )

