from pimc.sample import sampleModule, ensemble_cheating_sampleModule
from MCTS.is_node import ISMCTS_Abstract_Node
from MCTS.modules import Abstract_Default_MCTS_Module
from QLearn.state_translate import translate

from scipy.special import softmax
from copy import deepcopy
from math import sqrt, log
import numpy as np
from tensorflow import keras
import random

class QNetwork_MCTS(Abstract_Default_MCTS_Module):

    def __init__(self, q_network = None, load_q_network = None, exploration_constant = 0.7, softmax = True):
        self.softmax = softmax
        self.exploration_constant = exploration_constant
        if q_network:
            self.q_network = q_network
        elif load_q_network:
            self.q_network = keras.models.load_model(load_q_network)
        else:
            raise ValueError("Must Provide a q_network")
        self.q_network.compile(optimizer="adam", loss="huber")


    def __call__(self, rootstate, itermax= 100, time_limit = None, return_rootnode = False):
        self.rootnode = QLearning_Node(softmax = self.softmax)
        self.rootnode.set_additional_info(rootstate, self.q_network)
        self.itermax = itermax
        self.time_limit = time_limit
        self.return_rootnode = return_rootnode
        self.sampleModule = ensemble_cheating_sampleModule

        x = self.run_General_SO_ISMCTS(rootstate)
        if return_rootnode:
            return self.rootnode
        else:
            return x

    def __str__(self):
        return "QNetwork Perfect Information MCTS"

class QLearning_Node(ISMCTS_Abstract_Node):
    """
    A special Node in the GameTree, assuming you are playing with the Q-network enabled.
    """
    def __init__(self, softmax = True, *args, **kwargs):
        self.vector = None
        self.softmax = softmax
        super().__init__(*args, **kwargs)

    def _simulate(self, state):
        while not state.game_over():  # while state is non-terminal
            vector = np.array(self.q_network(translate(state))[0])
            LM = state.legal_moves()
            vec = vector[[c.idx() for c in LM]]
            if self.softmax:
                m = random.choices(LM,softmax(vec))[0]
            else:
                m = LM[np.argmax(vec)]
            state.result(m)
        return state

    def select_untried_moves(self, state):
        lst = self.get_untried_moves(state.legal_moves())
        vec = self.vector[[c.idx() for c in lst]]
        if self.softmax:
            return random.choices(lst,softmax(vec))[0]
        else:
            m = np.argmax(vec)
            return lst[m]
        
    def add_child(self, m, p):
        """ Add a new child node for the move m.
            Return the added child node
        """
        n = QLearning_Node(move=m, parent=self, playerJustMoved=p, softmax = self.softmax)
        new_state = deepcopy(self.state)
        new_state = new_state.result(m)
        n.set_additional_info(new_state, self.q_network)
        self.childNodes.append(n)
        return n

    def set_additional_info(self, state, q_network):
        self.set_q_network(q_network)
        self.set_state(state)
        

    def set_state(self, state):
        self.state = deepcopy(state)
        self.vector = np.array(self.q_network(translate(state))[0])

    def set_q_network(self, q_network):
        self.q_network = q_network

    def _OLD_select_child_UCB(self, state, exploration=0.7):
        """ Use the UCB1 formula to select a child node, filtered by the given list of legal moves.
            exploration is a constant balancing between exploitation and exploration, with default value 0.7 (approximately sqrt(2) / 2)
        """

        legalMoves = state.legal_moves()

        # Filter the list of children by the list of legal moves
        legalChildren = [child for child in self.childNodes if child.move in legalMoves]

        # Get the child with the highest UCB score
        s = max(
            legalChildren,
            key=lambda c: float(c.wins) / float(c.visits)
            + max(min(1+self.vector[[c.move.idx()]], 1),0.1) * exploration * sqrt(log(c.avails) / float(c.visits))
        )

        # Update availability counts -- it is easier to do this now than during backpropagation
        for child in legalChildren:
            child.avails += 1

        # Return the child selected above
        return s