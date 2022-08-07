"""
This module contains the definition of types fundamental to card games,
most notably the type Card.
"""

import sys
from random import shuffle

from enum import Enum

class OrderedEnum(Enum):

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class Suit(OrderedEnum):

    clubs = 0
    diamonds = 1
    spades = 2
    hearts = 3

    def __repr__(self):
        if sys.stdout.encoding in ['cp437', 'cp850']:
            # These are the correct unicode symbols in cp437 or cp850 encoding
            # They don't work for 1252 of utf8
            return [chr(5), chr(4), chr(6), chr(3)][self.value]
        else:
            return [' of clubs', ' of diamonds', ' of spades', ' of hearts'][self.value]


class Rank(OrderedEnum):

    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13
    ace = 14

    def __repr__(self):
        if self.value <= 10:
            return str(self.value)
        else:
            return ['J', 'Q', 'K', 'A'][self.value - 11]


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return repr(self.rank) + repr(self.suit)

    def __lt__(self, other):
        return (self.suit, self.rank) < (other.suit, other.rank)

    def __eq__(self, other):
        return (self.suit, self.rank) == (other.suit, other.rank)

    def card_points(self):
        """
        Returns the number of points the card is worth. None values return 0
        """
        if self is None:
            return 0
        if self.suit == Suit.spades and self.rank == Rank.queen:
            return 13
        return (1 if self.suit == Suit.hearts else 0 )
        
    def qs(self):
        """
        Returns True if the card is the Queen of Spades.
        """
        return self.rank == Rank.queen and self.suit == Suit.spades

    def h(self):
        """
        Returns True if the card is a heart.
        """
        return self.suit == Suit.hearts

    def eq(self, suit, rank):
        """Returns True if the suit and rank is equal to the card provided."""
        return self.suit == suit and self.rank == rank

    def idx(self):
        """
        Returns the index of the Card.

        0-12 represent Clubs
        13-25 represent Diamonds
        26-38 represent Spades
        39-51 represent Hearts

        Within each suit the index is ordered largest to smallest.
        """
        return int(self.suit.value) * 13 + int(self.rank.value) - 2

    def __hash__(self):
        return hash((self.suit, self.rank))

    def abbrv(self):
        return repr(self.rank) + ['C', 'D', 'S', 'H'][self.suit.value]

class Deck:

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    def deal(self):
        """
        Shuffles the cards and returns 4 lists of 13 cards.
        """
        shuffle(self.cards)
        for i in range(0, 52, 13):
            yield sorted(self.cards[i:i + 13])

def winning_index(leading_suit, trick):
        """
        Determine the index of the card that wins the trick.
        trick is a list of four Cards, i.e. an entire trick.
        """
        result = 0
        result_rank = Rank.two
        for i, card in enumerate(trick):
            if card is not None:
                if card.suit == leading_suit and card.rank >= result_rank:
                    result = i
                    result_rank = card.rank

        return result

#not used so far
def inv_idx(idx):
    suit = idx // 13
    rank = idx % 13

    return Card(Suit(suit), Rank(rank + 2))