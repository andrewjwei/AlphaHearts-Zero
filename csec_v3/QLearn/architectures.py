import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import tensorflow.keras.initializers as initializers


def copy_weights(Copy_from, Copy_to):
    """
    Function to copy weights of a model to other
    """
    variables2 = Copy_from.trainable_variables
    variables1 = Copy_to.trainable_variables
    for v1, v2 in zip(variables1, variables2):
        v1.assign(v2.numpy())
        
def make_network_copy(network,state_dim, action_dim, constructor):
    n = constructor(state_dim, action_dim)
    copy_weights(network, n)
    return n

###########################             

def construct_q_network(state_dim: int, action_dim: int) -> keras.Model:
    """Construct the critic network with q-values per action as output"""
    inputs = layers.Input(shape=(state_dim,))  # input dimension
    hidden1 = layers.Dense(
        400, activation="relu", kernel_initializer=initializers.he_normal()
    )(inputs)
    hidden2 = layers.Dense(
        200, activation="relu", kernel_initializer=initializers.he_normal()
    )(hidden1)
    hidden3 = layers.Dense(
        100, activation="relu", kernel_initializer=initializers.he_normal()
    )(hidden2)
    q_values = layers.Dense(
        action_dim, kernel_initializer=initializers.Zeros(), activation="linear"
    )(hidden3)

    deep_q_network = keras.Model(inputs=inputs, outputs=[q_values])

    return deep_q_network

###########################             

def construct_q_network_v2(state_dim: int, action_dim: int) -> keras.Model:
    """Equivalent to PV_NET_1"""
    inputs = layers.Input(shape=(state_dim,))  # input dimension
    fc0 = layers.Dense(
        2048, activation="relu", kernel_initializer=initializers.he_normal()
    )(inputs)
    fc1 = layers.Dense(
        2048, activation="relu", kernel_initializer=initializers.he_normal()
    )(fc0)
    fc2 = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(fc1)

    h0a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(fc2)
    h0b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h0a)
    h0 = layers.Average()([h0b, fc2])

    h1a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h0)
    h1b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h1a)
    h1 = layers.Average()([h1b, h0])

    h2a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h1)
    h2b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h2a)
    h2 = layers.Average()([h2b, h1])

    h3a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h2)
    h3b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h3a)
    h3 = layers.Average()([h3b, h2])

    h4a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h3)
    h4b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h4a)
    h4 = layers.Average()([h4b, h3])

    h5a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h4)
    h5b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h5a)
    h5 = layers.Average()([h5b, h4])

    q_values = layers.Dense(
        action_dim, kernel_initializer=initializers.Zeros(), activation="linear"
    )(h5)

    deep_q_network = keras.Model(inputs=inputs, outputs=[q_values])

    return deep_q_network



###########################             

def construct_q_network_v3(state_dim: int, action_dim: int) -> keras.Model:
    """Equivalent to PV_NET_2"""
    inputs = layers.Input(shape=(state_dim,))  # input dimension
    fc0 = layers.Dense(
        2048, activation="relu", kernel_initializer=initializers.he_normal()
    )(inputs)
    fc1 = layers.Dense(
        2048, activation="relu", kernel_initializer=initializers.he_normal()
    )(fc0)
    fc2 = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(fc1)

    h0a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(fc2)
    h0b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h0a)
    h0 = layers.Average()([h0b, fc2])

    h1a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h0)
    h1b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h1a)
    h1 = layers.Average()([h1b, h0])

    h2a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h1)
    h2b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h2a)
    h2 = layers.Average()([h2b, h1])

    h3a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h2)
    h3b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h3a)
    h3 = layers.Average()([h3b, h2])

    h4a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h3)
    h4b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h4a)
    h4 = layers.Average()([h4b, h3])

    h5a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h4)
    h5b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h5a)
    h5 = layers.Average()([h5b, h4])

    h6a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h5)
    h6b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h6a)
    h6 = layers.Average()([h6b, h5])

    h7a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h6)
    h7b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h7a)
    h7 = layers.Average()([h7b, h6])

    h8a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h7)
    h8b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h8a)
    h8 = layers.Average()([h8b, h7])

    h9a = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h8)
    h9b = layers.Dense(
        512, activation="relu", kernel_initializer=initializers.he_normal()
    )(h9a)
    h9 = layers.Average()([h9b, h8])

    q_values = layers.Dense(
        action_dim, kernel_initializer=initializers.Zeros(), activation="linear"
    )(h9)

    deep_q_network = keras.Model(inputs=inputs, outputs=[q_values])

    return deep_q_network