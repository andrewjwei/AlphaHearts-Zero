import sys
sys.path.append(r'/vast/palmer/home.grace/ajw88/csec_v3')
import os
os.chdir(r'/vast/palmer/home.grace/ajw88')

from MCTS.modules import SO_ISMCTS, MO_ISMCTS, Cheating_MCTS
from hearts.game import GameState
from players.player import StupidPlayer
from players.compound_player import ISMCTS_Player, PIMCPlayer
from players.complex_player import ComplexCheatingPlayer
from hearts.game import GameState
from hearts.arena import PlayerGrid, FourPlayerArena
from MCTS.pimc_translator import PerfInfo_MCTS
from pimc.sample import ensemble_cheating_sampleModule

import pickle as pkl

import time
t = time.time()

import random
random.seed(491)

save_location = r'saves/fig0/fig0a.pkl'

d_arr = [0.5,0.7,1,1.5,2,3,5,7,10,20,30,50]
x = []
arena = FourPlayerArena(default_num_iterations = 100, multiprocessing = True)

for d in d_arr:
    player_1 = ComplexCheatingPlayer()
    player_2 = PIMCPlayer(PerfInfoValue = PerfInfo_MCTS(itermax = 20, module = Cheating_MCTS(exploration_constant = d)), n = 10)
    x.append(arena.winning_points(player_1, player_2,num_iterations = 100))
    print(time.time()-t)
    
    output = open(save_location, 'wb')
    pkl.dump((x,d_arr),output)
    output.close()