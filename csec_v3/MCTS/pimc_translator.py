from MCTS.modules import Cheating_MCTS
from pimc.perfInfoModule import AbstractPerfInfoModule

class PerfInfo_MCTS(AbstractPerfInfoModule):
    """Returns the PerfInfo Module needed for PIMC. For regular PIMC, use module = Cheating_MCTS."""

    def __init__(self, itermax = 100, time_limit = None, module = Cheating_MCTS()):
        self.itermax = itermax
        self.time_limit = time_limit
        self.module = module

    def __str__(self):
        return str(self.module)

    def precompute_state(self,state):
        self.rootnode =  self.module(state, itermax= self.itermax, time_limit = self.time_limit, return_rootnode=True)

    def __call__(self, state, action):
        return self.rootnode.find_child_q_value(action)


