from pimc.sample import sampleModule, ensemble_cheating_sampleModule
from MCTS.is_node import Node
import random
import time


    
###########################################

class MCTS_Module:
    def __init__(self,exploration_constant = 0.7):
        self.exploration_constant = exploration_constant

    def __call__(self, rootstate, itermax= 100, time_limit = None, return_rootnode = False):
        """
        Must return a card from the given rootstate.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Must return a descriptive String
        """
        raise NotImplementedError

    def _simulate(self, state):
        while not state.game_over():  # while state is non-terminal
            state.result(random.choice(state.legal_moves()))
        return state

    def _backprop(self, state, node):
        while node is not None:
            # backpropagate from the expanded node and work back to the root node
            node.update(state)
            node = node.parentNode
        return node

###########################################


class Abstract_Default_MCTS_Module(MCTS_Module):
    def run_General_SO_ISMCTS(self, rootstate):
        self.sample_state = self.sampleModule(rootstate)
        if self.itermax is not None:
            for i in range(self.itermax):
                state = self.run_General_SO_ISMCTS_iteration()
        else:
            t = time.time()
            while t + self.time_limit > time.time():
                state = self.run_General_SO_ISMCTS_iteration()
        
        return max(self.rootnode.childNodes, key=lambda c: c.visits).move 

    def run_General_SO_ISMCTS_iteration(self):
        node = self.rootnode

        # Determinize
        state = self.sample_state()

        # Select
        node, state = self._SO_select(node, state)

        # Expand
        untriedMoves = node.get_untried_moves(state.legal_moves())
        if untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            node, state = self._SO_expand(node, state)

        # Simulate
        state = self._simulate(state)

        # Backpropagate
        node = self._backprop(state, node)

    def _SO_select(self, node, state):
        while not state.game_over() and node.get_untried_moves(state.legal_moves()) == []:
            # node is fully expanded and non-terminal
            node = node.select_child_UCB(state, exploration = self.exploration_constant)
            state.result(node.move)

        return (node, state)

    def _SO_expand(self, node, state):
        m = node.select_untried_moves(state)
        player = state.next_player()
        state.result(m)
        node = node.add_child(m, player)  # add child and descend tree
        return (node, state)

###########################################


class Cheating_MCTS(Abstract_Default_MCTS_Module):
    def __call__(self, rootstate, itermax= 100, time_limit = None, return_rootnode = False):
        self.rootnode = Node()
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
        return "Perfect Information MCTS"

###########################################


class SO_ISMCTS(Abstract_Default_MCTS_Module):
    def __call__(self, rootstate, itermax= 100, time_limit = None, return_rootnode = False):
        self.rootnode = Node()
        self.itermax = itermax
        self.time_limit = time_limit
        self.return_rootnode = return_rootnode
        self.sampleModule = sampleModule
        x = self.run_General_SO_ISMCTS(rootstate)
        if return_rootnode:
            return self.rootnode
        else:
            return x

    def __str__(self):
        return "SO-ISMCTS"

###########################################


class MO_ISMCTS(MCTS_Module):
    def __call__(self, rootstate, itermax= 100, time_limit = None, return_rootnode = False):
        return self._MO_ISMCTS(rootstate, itermax, time_limit, return_rootnode)

    def __str__(self):
        return "MO-ISMCTS"

    def _MO_ISMCTS(self, rootstate, itermax, time_limit, return_rootnode = False):
        """ Conduct an ISMCTS search for itermax iterations starting from rootstate.
            Return the best move from the rootstate.
        """
        rootnodes = (Node(), Node(), Node(), Node())
        sample_state = sampleModule(rootstate)

        if itermax is not None:
            for i in range(itermax):

                state = self._MO_ISMCTS_iteration(rootnodes, sample_state)
        else:
            t = time.time()
            while t + time_limit > time.time():
                state = self._MO_ISMCTS_iteration(rootnodes, sample_state)     

        if return_rootnode:
            return rootnodes

        return max(rootnodes[state.next_player()].childNodes, key=lambda c: c.visits).move 
        # return the move that was most visited

    def _MO_ISMCTS_iteration(self, rootnodes, sample_state):
        nodes = list(rootnodes)

        # Determinize
        state = sample_state()

        # Select
        nodes, state = self._MO_select(nodes, state)

        # Expand
        untriedMoves = nodes[state.next_player()].get_untried_moves(state.legal_moves())
        if untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            nodes, state = self._MO_expand(nodes, state)

        # Simulate
        state = self._simulate(state)

        # Backpropagate
        for i in range(4):
            nodes[i] = self._backprop(state, nodes[i])

        return state

    def _MO_select(self, nodes, state):
        while not state.game_over() and nodes[state.next_player()].get_untried_moves(state.legal_moves()) == []:
            # node is fully expanded and non-terminal
            nodes[state.next_player()] = nodes[state.next_player()].select_child_UCB(state, exploration = self.exploration_constant)

            m = nodes[state.next_player()].move
            player = state.next_player()
            for i in range(4):
                nodes[i] = nodes[i].find_or_add_child(m, player)  # add child and descend tree
            state.result(nodes[state.next_player()].move)

        return (nodes, state)



    def _MO_expand(self, nodes, state):
        m = nodes[state.next_player()].select_untried_moves( state)
        player = state.next_player()
        state.result(m)
        for i in range(4):
            nodes[i] = nodes[i].find_or_add_child(m, player)  # add child and descend tree
        return (nodes, state)


