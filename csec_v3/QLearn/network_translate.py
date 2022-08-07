from pimc.sample import sampleModule
from pimc.PerfInfoQValue import PerfInfoQValue
from players.compound_player import PIMCPlayer, ISMCTS_Player
from players.CheatQ_player import CheatQ_Player
from MCTS.QModule import QNetwork_MCTS
from MCTS.pimc_translator import PerfInfo_MCTS


def select_action_decorator(q_network):
    """
    This decorator, once applied to a q-network, will return a cheating player that plays the game according to the q-network.
    """
    return CheatQ_Player(q_network)

def select_pimc_action_decorator(q_network):
    """
    This decorator, once applied to a q-network, will return a PIMC player that plays the game according to the q-network.
    """
    return PIMCPlayer(sampleModule,PerfInfoQValue(q_network))

def select_perfect_mcts_action_decorator(q_network):
    """
    This decorator, once applied to a q-network, will return a MCTS player that plays the game according to the MCTS algorithm, adjusted by q-values.
    """
    return ISMCTS_Player(QNetwork_MCTS(q_network, exploration_constant = 1.0), n = 20)

def select_pimc_mcts_action_decorator(q_network):
    """
    This decorator, once applied to a q-network, will return a PIMC player that plays the game according to the MCTS algorithm, adjusted by q-values.
    """
    return PIMCPlayer(sampleModule,PerfInfo_MCTS(module=QNetwork_MCTS(q_network, exploration_constant = 1.0), itermax=20))


def select_perfect_mcts_EVAL_decorator(q_network):
    """
    This decorator, once applied to a q-network, will return a MCTS player that plays the game according to the MCTS algorithm, adjusted by q-values.
    """
    return ISMCTS_Player(QNetwork_MCTS(q_network, exploration_constant = 1.0), n = 100)

def select_pimc_mcts_EVAL_decorator(q_network):
    """
    This decorator, once applied to a q-network, will return a PIMC player that plays the game according to the MCTS algorithm, adjusted by q-values.
    """
    return PIMCPlayer(sampleModule,PerfInfo_MCTS(module=QNetwork_MCTS(q_network, exploration_constant = 1.0), itermax=100))


def select_pimc_DEMO_decorator(q_network):
    """
    This decorator, once applied to a q-network, will return a PIMC player that plays the game according to the MCTS algorithm, adjusted by q-values.
    """
    return PIMCPlayer(sampleModule,PerfInfo_MCTS(module=QNetwork_MCTS(q_network, exploration_constant = 1.0), itermax=400), n = 25)