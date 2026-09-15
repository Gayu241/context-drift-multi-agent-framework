from abc import ABC, abstractmethod


class MemoryPolicy(ABC):
    """
    Abstract base class for all memory policies.
    """

    @abstractmethod
    def decide(self, drift_report, validation_report):
        pass


class ResearchMemoryPolicy(MemoryPolicy):
    """
    Memory policy proposed in the research.

    Decision Rules:

    NO_DRIFT       -> IGNORE
    LOW_DRIFT      -> SHORT_TERM
    MODERATE_DRIFT -> REFLECTION
    HIGH_DRIFT     -> EXPERIENCE
    """

    def decide(self, drift_report, validation_report):

        if not validation_report.is_valid:
            return "REJECT"

        level = drift_report.drift_level.upper()

        if level == "NO_DRIFT":
            return "IGNORE"

        if level == "LOW_DRIFT":
            return "SHORT_TERM"

        if level == "MODERATE_DRIFT":
            return "REFLECTION"

        if level == "HIGH_DRIFT":
            return "EXPERIENCE"

        return "IGNORE"