from players.player import Player
from QLearn.state_translate import best_legal_move,translate
import tensorflow as tf

class CheatQ_Player(Player):
    def __init__(self,q_network):
        self.q_network = q_network

    def play_card(self, game):
        return self.__call__(game.state)

    def __call__(self, state):
        """
        Must return a card from the given hand.
        """
        return best_legal_move(state,tf.stop_gradient(self.q_network(translate(state)))[0])

    def __str__(self):
        """
        Must return a descriptive String
        """
        return "Cheating Q Network"