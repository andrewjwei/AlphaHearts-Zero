import multiprocessing
from MCTS.modules import SO_ISMCTS, MO_ISMCTS, Cheating_MCTS
from MCTS.QModule import QNetwork_MCTS
from hearts.game import GameState
from players.player import StupidPlayer
from players.compound_player import ISMCTS_Player, PIMCPlayer
from hearts.game import GameState
from hearts.arena import PlayerGrid
from MCTS.pimc_translator import PerfInfo_MCTS
from pimc.sample import ensemble_cheating_sampleModule




grid = PlayerGrid([StupidPlayer(),
                    ISMCTS_Player(SO_ISMCTS(), n = 100),
                    ISMCTS_Player(MO_ISMCTS(), n = 100), 
                    ISMCTS_Player(Cheating_MCTS(), n = 100), 
                    PIMCPlayer(PerfInfoValue = PerfInfo_MCTS(itermax = 20), n = 10, multiprocessing = False), 
                    PIMCPlayer(sampleModule = ensemble_cheating_sampleModule, PerfInfoValue = PerfInfo_MCTS(itermax = 20), n = 10, multiprocessing = True),
                    ISMCTS_Player(QNetwork_MCTS(load_q_network = '/home/accts/ajw88/csec/perfect_info/4'), n = 20)
                    ],
                    GameState, verbose = True, multiprocessing=False)
grid(1)
print(str(grid))
print(grid.avg_points())