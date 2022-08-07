import sys
sys.path.append(r'/vast/palmer/home.grace/ajw88/csec_v3')
import os
os.chdir(r'/vast/palmer/home.grace/ajw88')
import shutil

from players.player import SimplePlayer
from players.complex_player import MoreComplexPlayer, ComplexCheatingPlayer
from players.compound_player import ISMCTS_Player
from MCTS.modules import Cheating_MCTS
from hearts.game import GameState
from QLearn.architectures import construct_q_network, construct_q_network_v2, construct_q_network_v3
from QLearn.network_translate import select_action_decorator, select_pimc_action_decorator, select_perfect_mcts_action_decorator, select_pimc_mcts_action_decorator
from QLearn.selfPlay import SelfPlay


if sys.argv[1]  == "--help":
    print("""
Mandantory Flags (First Argument)
 --help      Run this to get help.
 --perf      Neural networks trained for performance on perfect information games, saved in "/saves/perfect_info/"
 --pimc      Neural networks trained for performance on PIMC games, saved in "/saves/pimc/"
 --cmcts     Neural networks trained as a perfect information MCTS game, saved in "/saves/CMCTS/"
 --cmctspimc Neural networks trained as a PIMC MCTS game, saved in "/saves/CMCTSpimc/"
 
Optional Flags:
 -tl=100     Specify a training limit for the network. Default: 100
 -nt=pv24    Specify a neural network type to run on. This is by default pv24. Other options are pv16, fc. If these are specified, they are placed in their own subfolder.
 --reset     This will overwrite the current network stored in the folder. 
""")
else:
    NETWORK = construct_q_network_v3
    TRAINING_LIMIT = 100
    #select the network to train on
    
    if sys.argv[1]  == "--perf":
        SAVE_NETWORK = r'saves/perfect_info/pv24/'
        TRAINING_TYPE = select_action_decorator
        STARTING_AGENT = (ISMCTS_Player(Cheating_MCTS(), n = 100), None)
        
    elif sys.argv[1]  == "--pimc":
        SAVE_NETWORK = r'saves/pimc/pv24/'
        TRAINING_TYPE = select_pimc_action_decorator
        STARTING_AGENT = (ISMCTS_Player(Cheating_MCTS(), n = 100), None)
        
    elif sys.argv[1]  == "--cmcts":
        SAVE_NETWORK = r'saves/CMCTS/pv24/'
        TRAINING_TYPE = select_perfect_mcts_action_decorator
        STARTING_AGENT = (ISMCTS_Player(Cheating_MCTS(), n = 100), None)
        
    elif sys.argv[1]  == "--cmctspimc":
        SAVE_NETWORK = r'saves/CMCTSpimc/pv24/'
        TRAINING_TYPE = select_pimc_mcts_action_decorator
        STARTING_AGENT = (ISMCTS_Player(Cheating_MCTS(), n = 100), None)
        
    else:
        print("Must specify Mandantory Argument. See --help for details.")
    
    for x in sys.argv:
        if '-nt' in x:
            if x == '-nt=pv24':
                pass
            elif x == '-nt=pv16':
                NETWORK = construct_q_network_v2
                SAVE_NETWORK = SAVE_NETWORK[:-5]
                SAVE_NETWORK += 'pv16/'
            elif x == '-nt=fc':
                NETWORK = construct_q_network
                SAVE_NETWORK = SAVE_NETWORK[:-5]
                SAVE_NETWORK += 'fc/'
            else:
                print("Incorrect specification of '-nt'. Using default.")
            
    if ['-tl' in x for x in sys.argv]:
        if x[0:4] == '-tl=':
            try:
                TRAINING_LIMIT = int(x[4:])
            except ValueError:
                print("Incorrect specification of '-tl'. Using default.")
    
    if '--reset' in sys.argv:
        for file in os.scandir(SAVE_NETWORK):
            shutil.rmtree(file.path)
    
    start = max([int(i) for i in os.listdir(SAVE_NETWORK)], default = -1)
    if start != -1:
        STARTING_AGENT = (None, start)
 
    sp = SelfPlay(NETWORK, starting_state = GameState, checkpoint_path = SAVE_NETWORK, num_iterations = 52*64, verbose = True, network_translator= TRAINING_TYPE)
    if STARTING_AGENT[0] is not None:
        sp(bootstrap_opponent =STARTING_AGENT[0], training_limit=TRAINING_LIMIT)
    else:
        sp(starting_agent =SAVE_NETWORK + str(STARTING_AGENT[1]), training_limit=TRAINING_LIMIT, starting_agent_number = STARTING_AGENT[1])


        