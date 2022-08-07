import tensorflow as tf
import random
import tensorflow.keras as keras
from hearts.game import GameState
from QLearn.state_translate import best_legal_move, translate
from QLearn.network_translate import select_action_decorator
from copy import deepcopy
import numpy as np

class QTrainer:
    """This module will train a Q-Network"""
    
    # epsilon, gamma, get_reward
    def __init__(self, get_reward, starting_state = GameState,
        epsilon_start = 0.25, epsilon_decay = 0.001, epsilon_min = 0.05, 
        gamma = 0.99, learning_rate = 0.0001, batch_size = 32):
        """
        Initialize Hyperparameters for the Q-network training.
        get_reward is required for the reward function.
        starting_state is required for the default starting state.
        epsilon, gamma, learning_rate are also needed.
        """
        self.get_reward = get_reward
        self.starting_state = starting_state

        self.gamma = gamma
        self.learning_rate = learning_rate
        self.batch_size = batch_size

        self.epsilon = epsilon_start
        self.epsilon_start = epsilon_start
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        self.action_size = 52
        self.loss_function = keras.losses.Huber()
        self.max_memory = 10000

        self.reset_history()

    def load_history(self, gameplay_history):
        """
        Given gameplay_history, a 5-tuple with (state_history, old_state_history, action_history, rewards_history, done_history), this will add gameplay_history to the buffer.
        """
        self.state_history = self.state_history + (gameplay_history[0])
        self.old_state_history = self.old_state_history + (gameplay_history[1])
        self.action_history = self.action_history + (gameplay_history[2])
        self.rewards_history = self.rewards_history + (gameplay_history[3])
        self.done_history = self.done_history + (gameplay_history[4])

        self._check_max_memory()

    def reset_history(self):
        self.action_history = []
        self.state_history = []
        self.old_state_history = []
        self.rewards_history = []
        self.done_history = []

    def train_q_network(self, q_network : keras.Model, num_episodes : int, target_q_network = None, opponent_agent = None, verbose = False, add_new_episodes = True, training_frequency = 4):
        """
        Given a q-network, this function will run through num_episodes states to train the Q-network.
        num_episodes = number of states. To get number of games, divide by 52.
        opponent_agent = bootstrap agent to train against. If not provided, it will train against a copy of itself.
        verbose = Will print q-values every 100 states.
        add_new_episodes = Will add new episodes to the training Queue. If this is true, it will assume opponent plays with opponent opponent_agent and you will play with best_q_value
        training_frequency = Will determine how often new episodes will be added. Total training sessions = num_episodes/training_frequency
        """

        self.epsilon = self.epsilon_start

        # Define optimizer
        opt = tf.keras.optimizers.Adam(learning_rate=self.learning_rate, beta_1=0.3, beta_2=0.999)
        
        state = self.starting_state()
        
        for episode in range(num_episodes):

            if add_new_episodes:
                old_state = translate(state)

                "Obtain Q-values from network"
                q_values = q_network(old_state)

                "Select action using epsilon-greedy policy"
                sample_epsilon = np.random.rand()
                if sample_epsilon <= self.epsilon: # Select random action
                    action = random.choice(state.legal_moves())
                else: # Select action with highest Q-value
                    action = best_legal_move(state, q_values[0])

                self.epsilon = max(self.epsilon - self.epsilon_decay, self.epsilon_min)

                "Obtain next state and direct reward for selected action"
                if opponent_agent:
                    state, reward = self.get_reward(state, action, opponent_agent)
                else:
                    state, reward = self.get_reward(state, action, select_action_decorator(q_network))

                "Check if game is over."
                if state.game_over():
                    state = self.starting_state()

                "Save actions and states in replay buffer"
                self.action_history.append(action.idx())
                self.old_state_history.append(old_state)
                self.state_history.append(translate(state))
                self.done_history.append(state.game_over())
                self.rewards_history.append(reward)

            "Update every 4th frame and once batch size is over 32"
            if episode % training_frequency == 0 and len(self.action_history) > self.batch_size:

                "Get indices of samples for replay buffers"
                indices = np.random.choice(range(len(self.action_history)), size = self.batch_size)
                action_sample = np.array([self.action_history[i] for i in indices])
                done_sample = np.array([self.done_history[i] for i in indices])
                old_state_sample = np.array([self.old_state_history[i] for i in indices])
                state_translated_sample = np.array([self.state_history[i] for i in indices])
                rewards_sample = np.array([self.rewards_history[i] for i in indices])
                
                for i, s in enumerate(state_translated_sample):
                    if target_q_network is None:
                        updated_q_value = (rewards_sample[i] + self.gamma * q_network(s)[0]) * (1-done_sample[i])
                    else:
                        updated_q_value = (rewards_sample[i] + self.gamma * target_q_network(s)[0]) * (1-done_sample[i])
                    
                    mask = tf.one_hot(action_sample[i], self.action_size)
                    with tf.GradientTape() as tape:
                        q_values = q_network(old_state_sample[i])

                        q_action = tf.reduce_sum(tf.multiply(q_values, mask), axis = 1)
                        loss = self.loss_function(updated_q_value,q_action)

                        "Compute gradients"
                        grads = tape.gradient(loss, q_network.trainable_variables)

                    "Apply gradients to update network weights"
                    opt.apply_gradients(zip(grads, q_network.trainable_variables))

            # Print console output
            if np.mod(episode, 100) == 0:
                if verbose and add_new_episodes:
                    print("\n====== episode", episode, " Q Values ======")
                    print(["%.3f" % n for n in q_values[0][0:13]])
                    print(["%.3f" % n for n in q_values[0][13:26]])
                    print(["%.3f" % n for n in q_values[0][26:39]])
                    print(["%.3f" % n for n in q_values[0][39:52]])

            self._check_max_memory()


    def _check_max_memory(self):
        if len(self.rewards_history) > self.max_memory:
            x = len(self.rewards_history) - self.max_memory
            del self.rewards_history[:x]
            del self.old_state_history[:x]
            del self.state_history[:x]
            del self.action_history[:x]
            del self.done_history[:x]