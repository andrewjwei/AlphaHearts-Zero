import random
from copy import deepcopy
from scipy.sparse.csgraph import maximum_flow
from scipy.sparse import csr_matrix

from hearts.card import Suit, Rank, Card
from hearts.helper import getKnownVoid

class AbstractSampler:

    def __init__(self,state):
        """Creates a sample object, using the state given to determinize."""
        raise NotImplementedError

    @classmethod
    def info_string(cls):
        return cls.__str__(None)

    def __str__(self):
        raise NotImplementedError

    def __call__(self):
        """Once called, this function will return a new state based on the original state"""
        raise NotImplementedError

class sampleModule(AbstractSampler):

    def __str__(self):
        return "Uniform Random Determinization"

    def __init__(self,state):        
        self.state = deepcopy(state)
        self.remaining = [len(hand) if i != self.state.turn_idx else 0 for i, hand in enumerate(self.state.player_hands)]
        self.unknown_cards = []
        for i, l in enumerate(self.state.player_hands):
            if i != self.state.turn_idx:
                self.unknown_cards += l        

        self.knownVoid = getKnownVoid(state)

        self.fast = all([all([not row[i] for i in range(4)]) for row in self.knownVoid])
        self.player_hand_lengths = [len(self.state.player_hands[hand]) if hand != self.state.turn_idx else 0 for hand in range(4) ]

    def __call__(self):
        new_state = deepcopy(self.state)
        counter = [0,0,0,0]
        base_len = len(self.unknown_cards) + 2
        random.shuffle(self.unknown_cards)

        if self.fast:
            for idx, card in enumerate(self.unknown_cards):
                if counter[0] < self.player_hand_lengths[0]:
                    destination = 0
                elif counter[1] < self.player_hand_lengths[1]:
                    destination = 1
                elif counter[2] < self.player_hand_lengths[2]:
                    destination = 2
                elif counter[3] < self.player_hand_lengths[3]:
                    destination = 3
                new_state.player_hands[destination][counter[destination]] = card
                counter[destination] += 1

            return new_state
   
        self.matrix=  [[0 for i in range(base_len + 4)] for j in range(base_len + 4)]
        for idx, card in enumerate(self.unknown_cards):
            for hand in range(4):
                if hand != self.state.turn_idx:
                    if card.suit == Suit.clubs:
                        self.matrix[idx + 2][base_len + hand] = int(not self.knownVoid[hand][0])
                    elif card.suit == Suit.diamonds:
                        self.matrix[idx + 2][base_len + hand] = int(not self.knownVoid[hand][1])
                    elif card.suit == Suit.hearts:
                        self.matrix[idx + 2][base_len + hand] = int(not self.knownVoid[hand][2])
                    elif card.suit == Suit.spades:
                        self.matrix[idx + 2][base_len + hand] = int(not self.knownVoid[hand][3])

            self.matrix[0][idx + 2] = 1

        for hand in range(4):
            self.matrix[base_len + hand][1] = self.player_hand_lengths[hand]

        x = maximum_flow(csr_matrix(self.matrix), 0, 1).residual  #this component takes 0.0008 seconds to run

        # this component takes 0.0005 to 0.0010 seconds to run
        for idx, card in enumerate(self.unknown_cards):
            if x[(idx + 2,len(self.unknown_cards) + 0 + 2)] == 1:
                destination = 0
            elif x[(idx + 2,len(self.unknown_cards) + 1 + 2)] == 1:
                destination = 1
            elif x[(idx + 2,len(self.unknown_cards) + 2 + 2)] == 1:
                destination = 2
            elif x[(idx + 2,len(self.unknown_cards) + 3 + 2)] == 1:
                destination = 3
            else:
                raise ValueError("This should not happen")
            new_state.player_hands[destination][counter[destination]] = card
            counter[destination] += 1

        return new_state
             


class ensemble_cheating_sampleModule(AbstractSampler):
    """ Rather than sampling, this will always return a copy of the existing state. This is useful for ensemble cheating.
    """

    def __str__(self):
        return "Cheating Determinization"

    def __init__(self,state):        
        self.state = deepcopy(state)

    def __call__(self):
        return deepcopy(self.state)
             