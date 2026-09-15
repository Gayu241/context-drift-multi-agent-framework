from enum import Enum


class AdaptationAction(Enum):
    """
    Represents the adaptation strategy selected by the
    Adaptation Policy.
    """

    NONE = "None"

    REMIND_GOAL = "Remind Goal"

    RETRIEVE_MEMORY = "Retrieve Memory"

    REPAIR_BELIEF = "Repair Belief"

    REBUILD_CONTEXT = "Rebuild Context"