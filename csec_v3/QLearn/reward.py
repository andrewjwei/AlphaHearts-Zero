
def get_reward(state, action, opponent_agent):
    """Generate new state and reward for selected state-action pairing"""
    
    current_player = state.next_player()
    
    action = None
    
    #old player points, to calculate reward.
    old_player_points = state.player_pts[current_player]
    
    while (action is None or state.next_player() != current_player) and not state.game_over():
        action = opponent_agent(state)
        state.result(action)
        
    reward = (old_player_points - state.player_pts[current_player])/26
    
    return state, reward
