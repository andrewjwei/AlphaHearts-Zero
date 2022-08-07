from tensorflow import keras
from hearts.arena import FourPlayerArena
from QLearn.network_translate import select_action_decorator, select_pimc_action_decorator, select_perfect_mcts_action_decorator
from hearts.game import GameState
from players.player import SimplePlayer
from players.complex_player import ComplexCheatingPlayer
import time

arena = FourPlayerArena(GameState,default_num_iterations=100, verbose = False)

t = time.time()
LIM_A = 100
i = 0
while i < LIM_A:
    q_network = keras.models.load_model('/home/accts/ajw88/csec/perfect_info/' + str(i))
    print(arena.winning_points(ComplexCheatingPlayer(), select_perfect_mcts_action_decorator(q_network)))
    print(time.time()-t)
    #Negative means that Player 1 is better
    i += 1
