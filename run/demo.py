import sys

sys.path.append('csec_v3/')

from players.player import HumanPlayer
from players.compound_player import ISMCTS_Player
from MCTS.modules import Cheating_MCTS
from MCTS.QModule import QNetwork_MCTS
from hearts.game import GameState
from hearts.arena import Game
from QLearn.network_translate import select_pimc_DEMO_decorator
from tensorflow import keras

q_network = keras.models.load_model('example_nn')

pl = [HumanPlayer(), select_pimc_DEMO_decorator(q_network), select_pimc_DEMO_decorator(q_network), select_pimc_DEMO_decorator(q_network)]

x = [0,0,0,0]
while True:
    g = Game(pl, verbose=True)
    game_result = g.play()
    print("Most Recent Game Result: " + str(game_result))
    x = [game_result[i] + x[i] for i in range(4)]
    print("Results so far: " + str(x))