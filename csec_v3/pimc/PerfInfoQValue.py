from pimc.perfInfoModule import AbstractPerfInfoModule
from QLearn.state_translate import translate
import tensorflow as tf

class PerfInfoQValue(AbstractPerfInfoModule):
    def __init__(self, q_network):
        self.q_network = q_network

    def __str__(self):
        return "PIMC Q Network"

    def precompute_state(self,state):
        self.q_values = tf.stop_gradient(self.q_network(translate(state)))

    def __call__(self, state, action):
        return self.q_values[0, action.idx()]
