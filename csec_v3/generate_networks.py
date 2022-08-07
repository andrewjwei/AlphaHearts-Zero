from players.player import SimplePlayer
from players.complex_player import MoreComplexPlayer, ComplexCheatingPlayer
from players.compound_player import ISMCTS_Player
from MCTS.modules import Cheating_MCTS
from hearts.game import GameState
from QLearn.architectures import construct_q_network, construct_q_network_v2, construct_q_network_v3
from QLearn.network_translate import select_action_decorator, select_pimc_action_decorator, select_perfect_mcts_action_decorator
from QLearn.selfPlay import SelfPlay

NETWORK = construct_q_network
#select the network to train on
SAVE_NETWORK = '/home/accts/ajw88/csec/perfect_info/'
#select location to save network.
#locations include ... "/saves/temp/"
# For neural networks trained for performance on perfect information games, "/saves/perfect_info/"
# For neural networks trained for performance on PIMC games, "/saves/pimc/"
# For neural networks with Cheating MCTS as a starting bootstrap, instead of ComplexCheatingPlayer, "/saves/CMCTS_BOOT/"
TRAINING_TYPE = select_perfect_mcts_action_decorator
#select 'select_action_decorator' to train on neural networks trained for performance on perfect information games. [faster]
#select 'select_pimc_action_decorator' to train on neural networks trained for performance on PIMC games. [more close to reality]
i = ISMCTS_Player(Cheating_MCTS())
STARTING_AGENT = (i, None)
#STARTING_AGENT = (None, 0)
#select (Agent, None) if you want to start from scratch for a bootstrap agent.
#select (None, Integer) if you want to start from an already trained network in a series.


sp = SelfPlay(NETWORK, starting_state = GameState, checkpoint_path = SAVE_NETWORK, num_iterations = 52*64, verbose = True, network_translator= TRAINING_TYPE)
if STARTING_AGENT[0] is not None:
    sp(bootstrap_opponent =STARTING_AGENT[0], training_limit=None)
else:
    sp(starting_agent =SAVE_NETWORK + str(STARTING_AGENT[1]), training_limit=None)

