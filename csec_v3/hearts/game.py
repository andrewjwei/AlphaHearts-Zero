from hearts.card import Suit, Rank, Card, Deck, winning_index

class GameState:

    def __init__(self, player_hands = None):
        """
        Creates a GameState object. If player_hands is not specified, the deck will be created randomly.
        The player_index_with_two_of_clubs will be the first player to go.
        GameState represents the snapshot of a moment in the Game, containing all the histories and all important information of the game.
        """
        
        deck = Deck()
        if player_hands is not None:
            self.player_hands = player_hands
        else:
            self.player_hands = tuple(deck.deal())

        self.leader_idx = self.player_index_with_two_of_clubs()
        self.suit = None
        self.trick_nr = 0

        self.player_pts = [0 for _ in range(4)]
        self.trick = [None for _ in range(4)]
        self.turn_idx = self.leader_idx

        self.history = [[None,None,None,None] for _ in range(13)]
        self.trick_leader = [None for _ in range(13)]
        self.trick_winner = [None for _ in range(13)]
            

    def __str__(self):
        return str(self.player_hands[0]) + "\n" + str(self.player_hands[1]) + "\n" +str(self.player_hands[2]) + "\n" + str(self.player_hands[3]) + "\n" + "Leader: " + str(self.leader_idx) + " Pts: " + str(self.player_pts) + " Trick: " + str(self.trick)
    
    def move(self,card):
        """Alias for "result". """
        return self.result(card)

    def history_str(self):
        """Returns a string with the history of the game."""
        string = """"""
        for i in range(self.trick_nr):
            string += ("\nNew Trick led by Player " + str(self.trick_leader[i])) + "\n"
            for j in range(4):
                string += ("Player " + str((self.trick_leader[i] + j) % 4) + " Plays " + str(self.history[i][(self.trick_leader[i] + j) % 4])) + "\n"
            string += ("Trick won by Player " + str(self.trick_winner[i])) + "\n"

        string += "\n" + ('Results of this game:') + "\n"
        for i in range(4):
            string += ("Player " + str(i) + " got " + str(self.winner()[i]) + " points") + "\n"
        return string

    def result(self, card):   
        """
        Modifies the state of the game to the state of the game after the card has been played.
        Returns the current state (the self object).
        """     
        #record-keeping
        if self.turn_idx == self.leader_idx:
            self.trick_leader[self.trick_nr] = self.next_player()
        self.history[self.trick_nr][self.turn_idx] = card
        
        #gameplay
        if not card:
            raise ValueError("Card is None. State: " + str(self))
        if self.turn_idx == self.leader_idx:
            self.trick[self.turn_idx] = card
            self.player_hands[self.turn_idx].remove(card)
            self.turn_idx = (self.turn_idx + 1) % 4
            self.suit = card.suit
        else:
            if self.is_legal_move(card):
                self.trick[self.turn_idx] = card
                self.player_hands[self.turn_idx].remove(card)
                self.turn_idx = (self.turn_idx + 1) % 4
            else:
                raise ValueError("Card cannot be played.\n")
        
            if (self.turn_idx - self.leader_idx) % 4 == 0:
                winner = winning_index(self.suit, self.trick)
                #record-keeping
                self.trick_winner[self.trick_nr] = winner
                #gameplay
                self.leader_idx = winner
                self.turn_idx = self.leader_idx
                self.player_pts[self.leader_idx] += sum([c.card_points() for c in self.trick])
                self.trick = [None,None,None,None]
                self.suit = None
                self.trick_nr +=1
                
        

        
        
        return self

    def is_legal_move(self, card):
        """
        Return True if the given card is valid to play in given context, False otherwise.
        """
        if self.suit == None:
            return True
        # Suit must be followed unless player has none of that suit
        return card.suit == self.suit or all([card.suit != self.suit for card in self.player_hands[self.turn_idx]])

    def legal_moves(self):
        """
        Generates a list of legal moves
        """
        if self.turn_idx == self.leader_idx or all([c.suit != self.suit for c in self.player_hands[self.turn_idx]]):
            return self.player_hands[self.turn_idx]
        else:
            return [c for c in self.player_hands[self.turn_idx] if c.suit == self.suit]

    def legal_moves_v2(self, return_as_index = False):
        """
        Generates a list of legal moves, with added functionality.
        If return_as_index is true, this will generate a list of legal moves but represented as card indices rather than Card objects.
        """
        if return_as_index:
            if self.turn_idx == self.leader_idx or all([c.suit != self.suit for c in self.player_hands[self.turn_idx]]):
                return [c.idx() for c in self.player_hands[self.turn_idx]]
            else:
                return [c.idx() for c in self.player_hands[self.turn_idx] if c.suit == self.suit]
        else:
            if self.turn_idx == self.leader_idx or all([c.suit != self.suit for c in self.player_hands[self.turn_idx]]):
                return self.player_hands[self.turn_idx]
            else:
                return [c for c in self.player_hands[self.turn_idx] if c.suit == self.suit]

    def next_player(self):
        """
        Returns the ID of the next player to move.
        """
        return self.turn_idx

    def game_over(self):
        """
        Returns True if the game is over, False otherwise.
        """
        return self.trick_nr >= 13

    def winner(self, standardize = False):
        """
        Only valid if the GameState is terminal.
        Returns the total amount of points that are won per player.
        If standardize = True, returns 1-points/26, or the standardized value between 0 and 1 [1 representing winning, or getting 0 points]
        """
        if standardize:
            if max(self.player_pts) == 26:
                return [p/26 for p in self.player_pts]
            else:
                return [1 - p/26 for p in self.player_pts]
        
        if max(self.player_pts) == 26:
            return [26 - p for p in self.player_pts]
        else:
            return self.player_pts

    def is_initial(self):
        """Returns True if the GameState is initial."""
        return self.turn_idx == 0 and self.trick_nr == 0

    def player_index_with_two_of_clubs(self):
        two_of_clubs = Card(Suit.clubs, Rank.two)
        for i in range(4):
            if two_of_clubs in self.player_hands[i]:
                return i

        raise AssertionError('No one has the two of clubs. This should not happen.')

    