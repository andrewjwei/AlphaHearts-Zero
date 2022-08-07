import sys
sys.path.append(r'/vast/palmer/home.grace/ajw88/csec_v3')
import os
os.chdir(r'/vast/palmer/home.grace/ajw88')

from tensorflow import keras
from hearts.game import GameState
from QLearn.network_translate import select_perfect_mcts_EVAL_decorator, select_pimc_mcts_EVAL_decorator
from hearts.arena import FourPlayerArena
from players.complex_player import ComplexCheatingPlayer

import pickle as pkl

import random
random.seed(491)

arena = FourPlayerArena(GameState,default_num_iterations=100, verbose = True)


if sys.argv[1]  == "--help":
    print("""
Mandantory Flags (First Argument)
 --help      Run this to get help.
 --perf      Neural networks trained for performance on perfect information games, saved in "/saves/perfect_info/"
 --pimc      Neural networks trained for performance on PIMC games, saved in "/saves/pimc/"
 --cmcts     Neural networks trained as a perfect information MCTS game, saved in "/saves/CMCTS/"
 --cmctspimc Neural networks trained as a PIMC MCTS game, saved in "/saves/CMCTSpimc/"

Optional Flags:
 -nt=pv24        Specify a neural network type to run on. This is by default pv24. Other options are pv16, fc.
 --cheat         This will make the network play in perfect information, without determinization.
 --reset         This will overwrite the current saves stored in the folder
 -eval=5         Specify a the frequency of evaluation. This is by default 5.

 File Save Locations:  'saves/fig2/[flag1]_[network type]_[cheat flag].pkl'
                  eg.  'saves/fig2/perf_pv24.pkl'
""")
else:
    
    if sys.argv[1]  == "--perf":
        data_save_location = r'saves/perfect_info/pv24/'
        file_save_location = r'saves/fig2/perf_pv24'
        
    elif sys.argv[1]  == "--pimc":
        data_save_location = r'saves/pimc/pv24/'
        file_save_location = r'saves/fig2/pimc_pv24'

    elif sys.argv[1]  == "--cmcts":
        data_save_location = r'saves/CMCTS/pv24/'
        file_save_location = r'saves/fig2/cmcts_pv24'

    elif sys.argv[1]  == "--cmctspimc":
        data_save_location = r'saves/CMCTSpimc/pv24/'
        file_save_location = r'saves/fig2/cmctspimc_pv24'
    else:
        print("Must specify Mandantory Argument. See --help for details.")
        exit(0)
    
    for x in sys.argv:
        if '-nt' in x:
            if x == '-nt=pv24':
                pass
            elif x == '-nt=pv16':
                data_save_location = data_save_location[:-5]
                data_save_location += 'pv16/'
                file_save_location = file_save_location[:-5]
                file_save_location += '_pv16'
                
            elif x == '-nt=fc':
                data_save_location = data_save_location[:-5]
                data_save_location += 'fc/'
                file_save_location = file_save_location[:-5]
                file_save_location += '_fc'
                
            else:
                print("Incorrect specification of '-nt'. Using default.")
                
    DECORATOR = select_pimc_mcts_EVAL_decorator
    
    if '--cheat' in sys.argv:
        DECORATOR = select_perfect_mcts_EVAL_decorator
        file_save_location += "_cheat"
        

   
    GAP = 5
    for x in sys.argv:
        if '-eval=' in x:
            if x != '-eval=5':
                try:
                    GAP = int(x[6:])
                    file_save_location += ("_" + str(GAP))
                except TypeError:
                    print("Incorrect specification of '-eval'. Using default of 5.")
                
                
                
    file_save_location += '.pkl'
    
    
    if not os.path.isfile(file_save_location):
        x = []
    else:
        if '--reset' in sys.argv:
            os.remove(file_save_location)
            x = []
        else:
            pkl_file = open(file_save_location, 'rb')
            x = pkl.load(pkl_file)
            pkl_file.close()
    
    print("Output will be at " + file_save_location)
    i = len(x) * GAP
    while i <= max([int(i) for i in os.listdir(data_save_location)], default = -1):
        print("Running network " + data_save_location + str(i))
        q_network = keras.models.load_model(data_save_location + str(i))
        x.append(arena.winning_points(ComplexCheatingPlayer(), DECORATOR(q_network)))  #change to pimc_action_decorator later
        #Negative means that Player 1 is better
        i += GAP

        output = open(file_save_location, 'wb')
        pkl.dump(x,output)
        output.close()
    
 

        