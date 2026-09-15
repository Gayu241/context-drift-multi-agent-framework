import copy
import random

from drift_injection.drift_types import DriftType


class DriftInjector:

    def __init__(self):

        self.value_map = {
            "pricerange": ["cheap", "moderate", "expensive"],
            "area": ["north", "south", "east", "west", "centre"],
            "parking": ["yes", "no"],
            "internet": ["yes", "no"],
            "stars": ["1", "2", "3", "4", "5"],
            "food": ["italian", "indian", "chinese", "british", "thai", "japanese"],
            "destination": [
                "cambridge",
                "ely",
                "london",
                "birmingham new street",
                "stansted airport"
            ],
            "departure": [
                "cambridge",
                "ely",
                "london",
                "kings lynn"
            ],
            "day": [
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday"
            ],
            "people": ["1", "2", "3", "4", "5", "6"],
            "stay": ["1", "2", "3", "4", "5"],
            "leaveAt": [
                "08:00",
                "09:30",
                "11:00",
                "13:00",
                "16:45",
                "19:00"
            ],
            "arriveBy": [
                "09:00",
                "10:30",
                "12:00",
                "15:00",
                "18:00",
                "21:00"
            ],
        }

        self.contradiction_map = {
            "yes": "no",
            "no": "yes",
            "cheap": "expensive",
            "expensive": "cheap",
            "moderate": "expensive",
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east",
            "centre": "north",
        }

    def inject(self, belief_state, drift_type):

        belief = copy.deepcopy(belief_state)

        if not belief.slots:
            return belief

        if drift_type == DriftType.SLOT_UPDATE:
            self.slot_update(belief)

        elif drift_type == DriftType.SLOT_INSERTION:
            self.slot_insert(belief)

        elif drift_type == DriftType.SLOT_DELETION:
            self.slot_delete(belief)

        elif drift_type == DriftType.CONTRADICTION:
            self.contradiction(belief)

        elif drift_type == DriftType.GOAL_DRIFT:
            self.goal_drift(belief)

        elif drift_type == DriftType.MULTI_SLOT:
            self.multi_slot(belief)

        elif drift_type == DriftType.RANDOM:
            self.slot_update(belief)

        return belief

    def slot_update(self, belief):

        slots = list(belief.slots.keys())

        if not slots:
            return

        candidates = [
            slot
            for slot in slots
            if slot in self.value_map
            and len(self.value_map[slot]) > 1
        ]

        slot = random.choice(candidates or slots)
        current = str(belief.slots[slot])

        if slot in self.value_map:

            alternatives = [
                value
                for value in self.value_map[slot]
                if str(value).lower() != current.lower()
            ]

            if alternatives:
                belief.slots[slot] = random.choice(alternatives)
                return

        belief.slots[slot] = f"{current}_changed"

    def slot_insert(self, belief):

        candidates = [
            slot
            for slot in self.value_map
            if slot not in belief.slots
        ]

        if candidates:

            slot = random.choice(candidates)

            belief.slots[slot] = random.choice(
                self.value_map[slot]
            )

            return

        synthetic = "context_extra"
        counter = 1

        while synthetic in belief.slots:
            counter += 1
            synthetic = f"context_extra_{counter}"

        belief.slots[synthetic] = "additional_context"

    def slot_delete(self, belief):

        if not belief.slots:
            return

        slot = random.choice(
            list(belief.slots.keys())
        )

        del belief.slots[slot]

    def contradiction(self, belief):

        if not belief.slots:
            return

        candidates = []

        for slot, value in belief.slots.items():

            value_lower = str(value).lower()

            if value_lower in self.contradiction_map:
                candidates.append(slot)

        if candidates:

            slot = random.choice(candidates)

            current = str(
                belief.slots[slot]
            ).lower()

            belief.slots[slot] = self.contradiction_map[current]

            return

        slot = random.choice(
            list(belief.slots.keys())
        )

        current = str(
            belief.slots[slot]
        )

        if slot in self.value_map:

            alternatives = [
                value
                for value in self.value_map[slot]
                if str(value).lower() != current.lower()
            ]

            if alternatives:

                belief.slots[slot] = random.choice(
                    alternatives
                )

                return

        belief.slots[slot] = f"contradictory_{current}"

    def goal_drift(self, belief):

        goal_slots = [
            "destination",
            "departure",
            "day",
            "people",
            "stay",
            "pricerange",
            "area",
            "food",
        ]

        candidates = [
            slot
            for slot in goal_slots
            if slot in belief.slots
        ]

        if candidates:

            slot = random.choice(candidates)

            if slot in self.value_map:

                current = str(
                    belief.slots[slot]
                )

                alternatives = [
                    value
                    for value in self.value_map[slot]
                    if str(value).lower() != current.lower()
                ]

                if alternatives:

                    belief.slots[slot] = random.choice(
                        alternatives
                    )

                    return

        self.slot_update(belief)

    def multi_slot(self, belief):

        original = copy.deepcopy(
            belief.slots
        )

        self.slot_update(belief)

        self.slot_insert(belief)

        if belief.slots == original:
            self.contradiction(belief)

        if belief.slots == original:
            self.slot_update(belief)