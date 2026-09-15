"""
multiwoz_adapter.py

Adapter for converting MultiWOZ 2.4 dialogues into the unified
Conversation representation used throughout the project.
"""

import json
import random
from pathlib import Path

from core.conversation import Conversation
from core.turn import Turn
from core.belief_state import BeliefState
from core.memory import Memory


class MultiWOZAdapter:

    def __init__(self, dataset_path: str):

        self.dataset_path = Path(dataset_path)

        self.dialogues = {}

        self.load_dataset()

    # =====================================================

    def load_dataset(self):

        if not self.dataset_path.exists():

            raise FileNotFoundError(self.dataset_path)

        with open(

            self.dataset_path,

            "r",

            encoding="utf-8"

        ) as f:

            self.dialogues = json.load(f)

        print(

            f"Loaded {len(self.dialogues)} MultiWOZ dialogues."

        )

    # =====================================================

    def list_dialogue_ids(self):

        return list(self.dialogues.keys())

    def get_random_dialogue(self):

        return random.choice(self.list_dialogue_ids())

    def get_dialogue(self, dialogue_id):

        return self.dialogues[dialogue_id]

    # =====================================================

    def to_conversation(self, dialogue_id):

        raw = self.get_dialogue(dialogue_id)

        conversation = Conversation(

            conversation_id=dialogue_id,

            dataset="MultiWOZ"

        )

        conversation.memory = Memory()

        conversation.domains = self._extract_domains(raw)

        conversation.goal = raw["goal"]

        conversation.turns = self._extract_turns(raw)

        conversation.belief_states = self._extract_belief_states(raw)

        return conversation

    # =====================================================

    def _extract_domains(self, raw):

        domains = []

        for domain, goal in raw["goal"].items():

            if domain in [

                "message",

                "topic"

            ]:

                continue

            if goal:

                domains.append(domain)

        return domains

    # =====================================================

    def _extract_turns(self, raw):

        turns = []

        for idx, turn in enumerate(raw["log"]):

            speaker = "USER" if idx % 2 == 0 else "SYSTEM"

            turns.append(

                Turn(

                    turn_id=idx,

                    speaker=speaker,

                    utterance=turn["text"],

                    metadata=turn["metadata"]

                )

            )

        return turns

    # =====================================================

    def _extract_belief_states(self, raw):

        beliefs = []

        for idx, turn in enumerate(raw["log"]):

            metadata = turn["metadata"]

            if not metadata:

                continue

            for domain, state in metadata.items():

                semi = state.get("semi", {})

                booking = state.get("book", {})

                # ------------------------------------------
                # Remove empty values
                # ------------------------------------------

                clean_slots = {

                    k: v

                    for k, v in semi.items()

                    if str(v).strip() not in [

                        "",

                        "not mentioned"

                    ]

                }

                clean_booking = {

                    k: v

                    for k, v in booking.items()

                    if str(v).strip() not in [

                        "",

                        []

                    ]

                }

                # ------------------------------------------
                # Skip empty belief states
                # ------------------------------------------

                if not clean_slots and not clean_booking:

                    continue

                beliefs.append(

                    BeliefState(

                        turn_id=idx,

                        domain=domain,

                        slots=clean_slots,

                        booking=clean_booking,

                        metadata=state

                    )

                )

        return beliefs