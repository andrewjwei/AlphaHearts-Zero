import sys
sys.path.append(r'/vast/palmer/home.grace/ajw88/csec_v3')
import os
os.chdir(r'/vast/palmer/home.grace/ajw88')
import sys

from MCTS.modules import SO_ISMCTS, MO_ISMCTS, Cheating_MCTS
from MCTS.QModule import QNetwork_MCTS
from MCTS.pimc_translator import PerfInfo_MCTS
from hearts.game import GameState
from players.player import StupidPlayer, SimplePlayer
from players.compound_player import ISMCTS_Player, PIMCPlayer
from players.complex_player import MoreComplexPlayer, ComplexCheatingPlayer
from hearts.game import GameState
from hearts.arena import PlayerGrid, FourPlayerArena
from pimc.sample import ensemble_cheating_sampleModule
from QLearn.network_translate import select_pimc_mcts_EVAL_decorator, select_perfect_mcts_EVAL_decorator

from tensorflow import keras
import pickle as pkl

import time
t = time.time()

import random
random.seed(491)

opp_list = [StupidPlayer(), SimplePlayer(), MoreComplexPlayer(), 
                    PIMCPlayer(PerfInfoValue = PerfInfo_MCTS(itermax = 100), n = 10),
                    ComplexCheatingPlayer(),
                    ISMCTS_Player(Cheating_MCTS(), n = 100)]

x = []
arena = FourPlayerArena(default_num_iterations = 100)


if sys.argv[1]  == "--help":
    print("""
if [ $1 == "--grid" ]; then
    echo "Running grid for all other agents"
    python driver/fig1/fig1.py
    exit 0
elif [ $1 == "--perf" ]; then
    echo "Running comparison for cheating agent"
    python driver/fig1/fig1b.py
    exit 0
elif [ $1 == "--pimc" ]; then
    echo "Running comparison for PIMC agent"
    python driver/fig1/fig1a.py
    exit 0
""")
else:
    
    if sys.argv[1]  == "--grid":
        file_save_location = r'saves/fig1/fig1Grid.pkl'
        if not os.path.isfile(file_save_location):
            grid = PlayerGrid(opp_list, GameState, verbose = True, save_location=file_save_location, multiprocessing = False)
        else:
            grid = PlayerGrid(load_location=file_save_location)
        grid(100)
        
    elif sys.argv[1]  == "--perf":
        file_save_location = r'saves/fig1/fig1b.pkl'
        if not os.path.isfile(file_save_location):
            x = []
        else:
            pkl_file = open(file_save_location, 'rb')
            x = pkl.load(pkl_file)
            pkl_file.close()
        
        i = len(x)
        while i < len(opp_list):
            player_2 = opp_list[i]
            q_network = keras.models.load_model(sys.argv[2])
            player_1 = select_perfect_mcts_EVAL_decorator(q_network)
            x.append(arena.winning_points(player_1, player_2,num_iterations = 100))
            print(time.time()-t)
            output = open(file_save_location, 'wb')
            pkl.dump(x,output)
            output.close()
            i +=1

    elif sys.argv[1]  == "--pimc":
        file_save_location = r'saves/fig1/fig1a.pkl'
        if not os.path.isfile(file_save_location):
            x = []
        else:
            pkl_file = open(file_save_location, 'rb')
            x = pkl.load(pkl_file)
            pkl_file.close()
        
        i = len(x)
        while i < len(opp_list):
            player_2 = opp_list[i]
            q_network = keras.models.load_model(sys.argv[2])
            player_1 = select_pimc_mcts_EVAL_decorator(q_network)
            x.append(arena.winning_points(player_1, player_2,num_iterations = 100))
            print(time.time()-t)
            output = open(file_save_location, 'wb')
            pkl.dump(x,output)
            output.close()
            i +=1

    else:
        print("Must specify Mandantory Argument. See --help for details.")
        exit(0)

