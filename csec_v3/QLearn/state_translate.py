import tensorflow as tf
import numpy as np

P1NN = 4 * 52
P2NN = 8 * 52
LEN = 52*8 + 14*4

def translate(state, points_idx = None, verbose = False):
    """
    This function will take in a state and return the Neural Network format.
    points_idx = Perspective of who are we trying to calculate points. IDK what happens if you put something in it.
    """
    if points_idx == None:
        points_idx = state.next_player()

    result = [0 for _ in range(LEN)]

    for idx, hand in enumerate(state.player_hands):
        for card in hand:
            result[((idx - points_idx) %4) * 52 + card.idx()] = 1

    for idx, card in enumerate(state.trick):
        if card:
            result[((idx - points_idx) %4) * 52 + P1NN + card.idx()] = 1

    for trick_nr, trick in enumerate(state.history):
        leader = state.trick_leader[trick_nr]
        for card in trick:
            if not card:
                continue
            elif card.h():
                result[(leader - points_idx %4) * 14 + P2NN + card.rank.value - 1] = 1   #1 ... 13
            elif card.qs():
                result[(leader - points_idx %4) * 14 + P2NN] = 1    #0
    
    if verbose:
        checksum = [0 for _ in range(52)]
        for i in range(8):
            print(result[i*52:i*52 + 52 -1])
            checksum = [checksum[idx] + val for idx, val in enumerate(result[i*52:i*52 + 52 -1])]
        
        for i in range(4):
            print(result[P2NN + i*14:P2NN + i*14 + 14 -1])

        print(checksum)
    return tf.constant([result])
        
def best_legal_move(state, vector):
    """
    Given a state and a length 52 vector of q values, this function will return the best legal move.
    """
    lm = state.legal_moves()
    vector = np.array(vector)
    m = np.argmax(vector[[c.idx() for c in lm]])
    return lm[m]
