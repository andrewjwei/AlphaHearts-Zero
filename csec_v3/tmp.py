from tensorflow import keras
from MCTS.pimc_translator import PerfInfo_MCTS
from hearts.arena import FourPlayerArena
from QLearn.network_translate import select_action_decorator, select_pimc_action_decorator, select_perfect_mcts_action_decorator
from hearts.game import GameState
from players.player import SimplePlayer
from players.complex_player import ComplexCheatingPlayer
from players.compound_player import ISMCTS_Player
from MCTS.modules import Cheating_MCTS
import time

arena = FourPlayerArena(GameState,default_num_iterations=100, verbose = False)

t = time.time()


class dummy:
    def __call__(self, *args, **kwds):
        return [[0 for _ in range(52)]]

    def compile(self, *args, **kwds):
        pass

y = arena.winning_points(ComplexCheatingPlayer(), select_perfect_mcts_action_decorator(dummy()))
#Negative means that Player 1 is better
print(y)
print(time.time()-t)

x = arena.winning_points(ComplexCheatingPlayer(), ISMCTS_Player(Cheating_MCTS(exploration_constant=1), n = 200) )
#Negative means that Player 1 is better
print(x)
print(time.time()-t)