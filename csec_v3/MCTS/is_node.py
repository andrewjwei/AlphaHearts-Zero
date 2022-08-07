from math import sqrt, log
import random


class ISMCTS_Abstract_Node:

    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
    """

    def __init__(self, move=None, parent=None, playerJustMoved=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.avails = 1
        self.playerJustMoved = (
            playerJustMoved
        )  # the only part of the state that the Node needs later

    def get_untried_moves(self, legalMoves):
        """ Return the elements of legalMoves for which this node does not have children.
        """

        # Find all moves for which this node *does* have children
        triedMoves = [child.move for child in self.childNodes]

        # Return all moves that are legal but have not been tried yet
        return [move for move in legalMoves if move not in triedMoves]



    def add_child(self, m, p):
        """ Add a new child node for the move m.
            Return the added child node
        """
        n = Node(move=m, parent=self, playerJustMoved=p)
        self.childNodes.append(n)
        return n

    def find_or_add_child(self, m, p):
        """ Either finds the child node which is a result of this move, or adds said child.
            Returns the child node
        """
        for c in self.childNodes:
            if c.move == m:
                return c
        n = self.add_child(m,p)
        return n

    def update(self, terminalState):
        """ Update this node - increment the visit count by one, and increase the win count by the result of terminalState for self.playerJustMoved.
        """
        self.visits += 1
        if self.playerJustMoved is not None:
            self.wins += 1 - terminalState.winner()[self.playerJustMoved]/26

    def __repr__(self):
        return "[M:%s W/V/A: %4f/%4i/%4i]" % (
            self.move,
            self.wins,
            self.visits,
            self.avails,
        )

    def tree_to_string(self, indent):
        """ Represent the tree as a string, for debugging purposes.
        """
        s = self.indent_string(indent) + str(self)
        for c in self.childNodes:
            s += c.tree_to_string(indent + 1)
        return s

    def indent_string(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def children_to_string(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s

    def find_child_q_value(self, move):
        for c in self.childNodes:
            if c.move == move:
                return c.wins/c.visits
        return 0


    def select_child_UCB(self, state, exploration=0.7):
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
            + exploration * sqrt(log(c.avails) / float(c.visits))
        )

        # Update availability counts -- it is easier to do this now than during backpropagation
        for child in legalChildren:
            child.avails += 1

        # Return the child selected above
        return s

    def select_untried_moves(self, state):
        raise NotImplementedError

class Node(ISMCTS_Abstract_Node):
    def select_untried_moves(self, state):
        return random.choice(self.get_untried_moves(state.legal_moves()))
