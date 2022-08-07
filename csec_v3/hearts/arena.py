from hearts.card import Deck
from hearts.game import GameState
from QLearn.state_translate import translate

import numpy as np
import time
from copy import deepcopy
import pickle as pkl
import multiprocessing
import functools
import numpy as np

class FourPlayerArena:
    def __init__(self , starting_state = GameState, verbose = False, default_num_iterations = 100, multiprocessing = False, keep_history = False):
        """
        Creates a FourPlayerArena Object. This object will allow for two players to match off against each other (in a NS vs EW configuration) to check the total amount of points one player is worth.
        
        Inputs:
        The starting_state parameter initiates each game. Default: GameState
        The verbose parameter will print every time a game is played. Default: False
        The default_num_iterations will indicate the default number of evaluations performed in the arena. Default = 100.
        multiprocessing is by default True. However, if players have a time limit this must be False.
        """
        self.starting_state = starting_state
        self.verbose = verbose
        self.multiprocessing = multiprocessing
        self.default_num_iterations = default_num_iterations
        self.keep_history = keep_history

    def fair_evaluate(self, player_1, player_2):
        """
        Plays a single game between two players in a NS vs EW configuration, returning the points to each player individually.
        Then, it repeats the same game, but with the player positions swapped.
        """
        deck = Deck()
        hand = (tuple(deck.deal()))
        if self.keep_history:
            results, history = self.evaluate(player_1,player_2,deck = deepcopy(hand))
            results2, history2 = self.evaluate(player_2,player_1,deck = deepcopy(hand))
            return [results[i] + results2[(i+1) % 4] for i in range(4)], history

        results = self.evaluate(player_1,player_2,deck = deepcopy(hand))
        results2 = self.evaluate(player_2,player_1,deck = deepcopy(hand))
        return [results[i] + results2[(i+1) % 4] for i in range(4)]
        


    def evaluate(self, player_1, player_2, deck = None):
        """
        Plays a single game between two players in a NS vs EW configuration, returning the points to each player individually.
        """

        network_dict = {0 : player_1, 1 : player_2, 2 : player_1, 3 : player_2}
        state = self.starting_state()

        if deck is not None:
            state.player_hands = deck

        t =  time.time()

        if self.keep_history:
            action_history = []
            state_history = []
            old_state_history = []
            rewards_history = []
            done_history = []
            prior_state_buffer = [None for _ in range(4)]
            prior_action_buffer = [None for _ in range(4)]
            old_player_points_buffer = [0 for _ in range(4)]
        
        while not state.game_over():
            current_player = state.next_player()
            network = network_dict[current_player]
            action = network(state)

            if self.keep_history:
                prior_state_buffer[current_player] = translate(state)
                prior_action_buffer[current_player] = action.idx()
                old_player_points_buffer[current_player] = state.player_pts[current_player]

            state = state.result(action)

            if self.keep_history and not state.game_over():
                next_player = state.next_player()
                if prior_state_buffer[next_player] is not None:
                    state_history.append(translate(state))
                    old_state_history.append(prior_state_buffer[next_player]) 
                    action_history.append(prior_action_buffer[next_player])
                    rewards_history.append((old_player_points_buffer[next_player] - state.player_pts[next_player])/26)
                    done_history.append(0)
        
        if self.keep_history and state.game_over():
            for i in range(4):
                state_history.append(translate(state))
                old_state_history.append(prior_state_buffer[i]) 
                action_history.append(prior_action_buffer[i])
                rewards_history.append((old_player_points_buffer[i] - state.player_pts[i])/26)
                done_history.append(1)
        

        if self.verbose:
            print("Game Results: " + str(state.player_pts) + " Results Evaluated in " + str(time.time() - t))
        
        if self.keep_history:
            return (state.winner(), (state_history, old_state_history, action_history, rewards_history, done_history))

        return state.winner()
    

    def iterate(self, num_iterations, player_1, player_2):
        """
        Plays num_iterations games between two players in a NS vs EW configuration, returning the points to each player individually.
        """
        rewards_list = [0,0,0,0]
        if self.multiprocessing:
            with multiprocessing.Pool(num_iterations) as p:
                rewards = p.map(functools.partial(self.fair_evaluate, player_1), [player_2 for _ in range(num_iterations)])
        else:
            rewards = map(functools.partial(self.fair_evaluate, player_1), [player_2 for _ in range(num_iterations)])
        
        if self.keep_history:
            state_history = []
            old_state_history = []
            action_history = []
            rewards_history = []
            done_history = []
            for r in rewards:

                rewards_list = [r[0][i] + rewards_list[i] for i in range(4)]
                state_history = state_history + (r[1][0])
                old_state_history = old_state_history + (r[1][1])
                action_history = action_history + (r[1][2])
                rewards_history = rewards_history + (r[1][3])
                done_history = done_history + (r[1][4])

            return (rewards_list, (state_history, old_state_history, action_history, rewards_history, done_history))
        
        for r in rewards:
            rewards_list = [r[i] + rewards_list[i] for i in range(4)]
        return rewards_list
    
    
    def get_winning_network(self, player_1, player_2, num_iterations = None):
        """
        Returns the winner between two players.
        If num_iterations is not specified, does so in default_num_iterations games.
        Returns -1 if player 1 is better. Returns 1 if player 2 is better.
        """
        if not num_iterations:
            num_iterations = self.default_num_iterations
        return np.sign(self.winning_points(player_1, player_2, num_iterations)) #higher score is worse!!

    def winning_points(self, player_1, player_2, num_iterations = None):
        """
        Returns the point difference between two players.
        If num_iterations is not specified, does so in default_num_iterations games.
        Returns negative if player 1 is better. Returns positive if player 2 is better.
        """
        if not num_iterations:
            num_iterations = self.default_num_iterations
        
        if not self.keep_history:
            results = self.iterate(num_iterations, player_1, player_2)
            diff = results[0] + results[2] - (results[1] + results[3])
            return diff #higher score is worse!!
        else:
            results = self.iterate(num_iterations, player_1, player_2)
            diff = results[0][0] + results[0][2] - (results[0][1] + results[0][3])
            return (diff,results[1]) #higher score is worse!!

class PlayerGrid:
    def __init__(self , players = None, starting_state = GameState, verbose = True, save_location = None, load_location = None, multiprocessing = True):
        """
        Creates a PlayerGrid Object. This object will allow for any number of players to match off against each other.
        
        Inputs if load_location is specified:
        This will load a grid object from memory. This is good for memorizing past games.

        Inputs if load_location is not specified:
        The players parameter is mandantory, and must be a list of players. Players will be indexed 0 onwards.
        The starting_state parameter initiates each game. Default: GameState
        The num_iterations parameter indicates the number of game iterations it takes to evaluate a pairing.
        The verbose parameter will print every time the game finishes evaluating a pairing. Default: True
        The multiprocessing parameter must be False if you are testing time limits. Otherwise, it is best on True.

        Outputs a function. Every time you call the function, the PlayerGrid will calculate the result of each pairing.
        """
        if load_location is not None:
            pkl_file = open(load_location, 'rb')
            loaded = pkl.load(pkl_file)
            pkl_file.close()
            print("Loaded from: " + load_location)
            self.players = loaded.players
            self.starting_state = loaded.starting_state
            self.verbose = loaded.verbose
            self.grid = loaded.grid
            self.num_iterations = loaded.num_iterations
            self.save_location = loaded.save_location
            self.multiprocessing = loaded.multiprocessing
        else:
            if players is None:
                raise ValueError("Players cannot be None if load_location is not specified.")
            self.players = players
            self.starting_state = starting_state
            self.verbose = verbose
            self.grid = [[0 for _ in players] for __ in players]
            self.num_iterations = 0
            self.save_location = save_location
            self.multiprocessing = multiprocessing

    def __call__(self, itermax = 100):
        """Every time you call the function, the PlayerGrid will calculate the result of each pairing."""
        
        if self.verbose:
            print("Running " + str(itermax) + " Iterations")
            print("Prior Iterations: " + str(self.num_iterations))
            for i, p in enumerate(self.players):
                print(str(i) + ": " + str(p))
        self.num_iterations += itermax

        arena = FourPlayerArena(self.starting_state, multiprocessing=self.multiprocessing)
        for i, player_1 in enumerate(self.players):
            for j, player_2 in  enumerate(self.players):
                if i < j:
                    t = time.time()
                    diff = arena.winning_points(player_1, player_2, num_iterations = itermax)
                    if self.verbose:
                        print(str(i) + " vs " + str(j) + " Results " + str(diff) + " Evaluated in " + str(time.time() - t) + " Seconds")
                    self.grid[i][j] = diff
                    self.grid[j][i] = -diff

        
        if self.save_location is not None:
            print("Saving to " + self.save_location)
            output = open(self.save_location, 'wb')
            pkl.dump(self,output)
            output.close()
        
        return self.grid

    def __str__(self):
        x = ""
        for row in zip(*self.grid):
            x += ((len(self.players) * '{:<10} ').format(*row)) + "\n"
        return x

    def avg_points(self, rel_to = None):
        """
        Returns the average points taken per game per player.
        If rel_to is specified, this is calculated relative to the the player at the index given.
        Reminder that positive values are worse.
        """
        lst = [sum(row)/len(self.players)/(self.num_iterations)/2 for row in self.grid]
        if rel_to is None:
            return lst

        return [i - lst[rel_to] for i in lst]


class Game:
    """"Allows you to play against various different player types."""

    def __init__(self, players, verbose=False):
        """
        players is a list of four players
        """
        self.verbose = verbose
        if len(players) != 4:
            raise ValueError('There must be four players.')
        self.players = players

        self.state = GameState()
        self.starting_state = deepcopy(self.state)

    def say(self, message, *formatargs):
        if self.verbose:
            print(message.format(*formatargs))
            
    def play(self, partial_stop = 52):
        """
        Simulate a single game and return a 4-tuple of the scores.
        """
        # Players and their hands are indentified by indices ranging from 0 till 4

        # Play the tricks:
        for i in range(partial_stop):
            if i % 4 == 0:
                if self.verbose:
                    print("\nNew Trick led by Player " + str(self.state.next_player()))
            card = self.players[self.state.next_player()].play_card(self)
            if not card:
                raise ValueError("Card is None. State: " + str(self.state))
            if self.verbose:
                print("Player " + str(self.state.next_player()) + " Plays " + str(card))
            self.state.result(card)
            if i % 4 == 3:
                if self.verbose:
                    print("Trick won by Player " + str(self.state.next_player()))

        # Print and return the results
        self.say('Results of this game:')
        for i in range(4):
            self.say('Player {} got {} points',
                     i,
                     self.state.winner()[i]
                     )

        return tuple(self.state.winner()[i] for i in range(4))

