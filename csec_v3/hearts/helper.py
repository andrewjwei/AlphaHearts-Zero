from hearts.card import Suit

def getKnownVoid(state):
    knownVoid = [[False for i in range(4)] for j in range(4)]
    for trick_nr, trick in enumerate(state.history):
        if state.trick_leader[trick_nr] != None:
            leading_suit = state.history[trick_nr][state.trick_leader[trick_nr]].suit
            for player_idx, card in enumerate(trick):
                if card is not None and leading_suit != card.suit:
                    if leading_suit == Suit.clubs:
                        knownVoid[player_idx][0] = True
                    elif leading_suit == Suit.diamonds:
                        knownVoid[player_idx][1] = True
                    elif leading_suit == Suit.hearts:
                        knownVoid[player_idx][2] = True
                    elif leading_suit == Suit.spades:
                        knownVoid[player_idx][3] = True
                state.trick_leader[trick_nr]
        else:
            break
    return knownVoid