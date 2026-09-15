from core.conversation import Conversation
from core.turn import Turn
from core.belief_state import BeliefState
from core.memory import Memory


conversation = Conversation(
    conversation_id="001",
    dataset="MultiWOZ"
)

conversation.memory = Memory()

conversation.add_turn(
    Turn(
        turn_id=1,
        speaker="USER",
        utterance="I need a cheap hotel."
    )
)

conversation.add_belief_state(
    BeliefState(
        turn_id=1,
        domain="hotel",
        slots={
            "price": "cheap",
            "parking": "yes"
        }
    )
)

print(conversation)
print()
print(conversation.latest_turn())
print()
print(conversation.latest_belief_state())
print()
print(conversation.memory)