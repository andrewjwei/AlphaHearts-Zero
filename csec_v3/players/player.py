"""This module containts the abstract class Player and some implementations."""
import random
from hearts.card import Suit,Rank,Card,Deck

class Player:

    """
    Abstract class defining the interface of a Computer Player.
    """

    def play_card(self, game):
        """
        Must return a card from the given hand.
        """
        return self.__call__(game.state)
        
    def __call__(self, state):
        """
        Must return a card from the given hand.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Must return a descriptive String
        """
        raise NotImplementedError



class StupidPlayer(Player):

    """
    Most simple player you can think of.
    It just plays random valid cards.
    """

    def __str__(self):
        return "Random Player"

    def __call__(self, state):
        """
        Must return a card from the given hand.
        """
        # Play first card that is valid
        if len(state.legal_moves()) > 0:
            c = random.choice(state.legal_moves())
            if c:
                return c
        raise AssertionError(
            'Apparently there is no valid card that can be played. This should not happen.'
        )

class HumanPlayer(Player):

    def __str__(self):
        return "Human Player"

    def __call__(self, state):
        """
        Must return a card from the given hand.
        """
        print("Your Cards are listed below.")
        for i, c in enumerate(state.player_hands[state.turn_idx]):
            if state.is_legal_move(c):
                print(str(c) + " Option #" + str(i))
            else:
                print(str(c) + " Not Legal")
        
        while True:
            try:
                i = input("What card do you want to play? >")
                if i == "debug0":
                    print()
                    print(state)
                    print()
                    raise IndexError
                if i == "debug1":
                    print(state.history_str())
                    raise IndexError

                try:
                    i = int(i)
                except ValueError:
                    raise IndexError
                    
                if not state.is_legal_move(state.player_hands[state.turn_idx][i]):
                    raise IndexError
                else:
                    raise ValueError
            except IndexError:
                pass
            except ValueError:
                return state.player_hands[state.turn_idx][i]

class SimplePlayer(Player):

    """
    This player has a notion of a card being undesirable.
    It will try to get rid of the most undesirable cards while trying not to win a trick.
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        if verbose:
            deck = Deck()
            deck.cards.sort(key=self.undesirability)
            self.say('Card undesirability: ')
            for card in deck.cards:
                self.say('{}: {}', card, self.undesirability(card))

    def __str__(self):
        return "Simple Heuristic Player"

    def say(self, message, *formatargs):
        if self.verbose:
            print(message.format(*formatargs))

    def undesirability(self, card):
        return (
            card.rank.value
            + (10 if card.suit == Suit.spades and card.rank >= Rank.queen else 0)
        )

    def __call__(self, state):        # Lead with a low card
        hand = state.player_hands[state.turn_idx]
        if state.leader_idx == state.turn_idx:
            hand.sort(key=lambda card: card.rank.value)
            return hand[0]

        if self.verbose:
            hand.sort(key=self.undesirability, reverse=True)
            self.say('Hand: {}', hand)
            self.say('Trick so far: {}', state.trick)

        # Safe cards are cards which will not result in winning the trick
        leading_suit = state.suit
        max_rank_in_leading_suit = Rank.two
        for card in state.trick:
            if card is not None:
                if card.suit == leading_suit:
                    max_rank_in_leading_suit = max(max_rank_in_leading_suit, card.rank)
        safe_cards = [card for card in state.legal_moves()
                      if card.suit != leading_suit or card.rank <= max_rank_in_leading_suit]

        if self.verbose:
            self.say('Valid cards: {}', state.legal_moves())
            self.say('Safe cards: {}', safe_cards)

        try:
            return safe_cards[0]
        except IndexError:
            queen_of_spades = Card(Suit.spades, Rank.queen)
            # Don't try to take a trick by laying the queen of spades
            if state.legal_moves()[0] == queen_of_spades and len(state.legal_moves()) > 1:
                return state.legal_moves()[1]
            else:
                return state.legal_moves()[0]




            
            