from players.player import Player
from pimc.pimc import PIMC
from pimc.sample import sampleModule
from MCTS.pimc_translator import PerfInfo_MCTS

class PIMCPlayer(Player):
    def __init__(self, sampleModule = sampleModule, PerfInfoValue = PerfInfo_MCTS(), n = 10, multiprocessing = False):
        self.pimc = PIMC(sampleModule,PerfInfoValue, n = n, multiprocessing = multiprocessing)
        self.str = "PIMC Player with sampleModule: " + sampleModule.info_string() + " PerfInfoValue: " + str(PerfInfoValue)

    def __str__(self):
        return self.str 

    def play_card(self,game):
        return self.__call__(game.state)

    def __call__(self, state):
        return self.pimc(state)

class ISMCTS_Player(Player):

    def __init__(self, ismcts_module, n = 100, time_limit = None, verbose=False):
        self.ismcts_module = ismcts_module
        self.n = n
        self.verbose = verbose
        self.time_limit = time_limit

    def __str__(self):
        return "ISMCTS Player with Module: " + str(self.ismcts_module)

    def play_card(self,game):
        return self.__call__(game.state)

    def __call__(self, state):
        """
        Must return a card from the given hand.
        """
        return self.ismcts_module(rootstate=state, itermax=self.n, time_limit = self.time_limit)

        