from hearts.helper import getKnownVoid
from hearts.card import Rank,Suit,Card
from players.player import Player

LST = (Suit.clubs, Suit.diamonds, Suit.hearts, Suit.spades)

def check_QS_gone(state):
    for trick_nr in range(state.trick_nr):
        for card in state.history[trick_nr]:
            if card.qs():
                return True
    return False

def max_safe_hand(state):
    if state.suit == None:
        raise ValueError("This cannot be calculated if we are at the leader")

    m = max([t for t in state.trick if t and t.suit == state.suit])
    safe_hands = [t for t in state.legal_moves() if t.rank < m.rank]
    if safe_hands == None:
        return None
    else:
        return max(safe_hands, default = None, key = lambda c : c.rank)

def max_excl_qs(state):
    return max([t for t in state.legal_moves() if not t.qs()], default = None, key = lambda c : c.rank)

def max_card(state):
    return max(state.legal_moves(), key = lambda c : c.rank)

def min_excl_qs(state):
    return min([t for t in state.legal_moves() if not t.qs()], default = None, key = lambda c : c.rank)

def min_card(state):
    return min(state.legal_moves(), key = lambda c : c.rank)

def provoke_spades(state):
    """Plays the highest Spade lower than Queen"""
    return max([t for t in state.legal_moves() if t.rank < Rank.queen and t.suit == Suit.spades], default = None, key = lambda c : c.rank)

def max_suit(state, suit):
    return max([t for t in state.legal_moves() if t.suit == suit], default = None, key = lambda c : c.rank)

def min_suit(state, suit):
    return min([t for t in state.legal_moves() if t.suit == suit], default = None, key = lambda c : c.rank)

def suit_counts(state):
    count = [0,0,0,0]
    for card in state.player_hands[state.turn_idx]:
        count[card.suit.value] += 1
    return count

def rounds_counts(state):
    count = [0,0,0,0]
    for trick_nr, leader in enumerate(state.trick_leader):
        if leader:
            card = state.history[trick_nr][leader]
            count[card.suit.value] += 1
    return count

def find_card(state, list_of_cards):
    hand = state.player_hands[state.turn_idx]
    for find_card in list_of_cards:
        for card in hand:
            if card == find_card:
                return card
    return None

def find_card_in_legal_moves(state, list_of_cards):
    hand = state.legal_moves()
    for find_card in list_of_cards:
        for card in hand:
            if card == find_card:
                return card
    return None


def default_low_card(state):
    SC = suit_counts(state)
    suit = LST[SC.index(min(SC))]
    x = min_suit(state, suit)
    if x and x.rank.value < Rank.ten.value:
        return x
    return min_card(state)

def dispose_card(state):
    hand = state.legal_moves()
    if check_QS_gone(state):
        x = find_card_in_legal_moves(state, [Card(Suit.hearts, Rank.ace), Card(Suit.hearts, Rank.king),
                              Card(Suit.clubs, Rank.ace), Card(Suit.diamonds, Rank.ace), Card(Suit.spades, Rank.ace),
                              Card(Suit.clubs, Rank.king), Card(Suit.diamonds, Rank.king), Card(Suit.spades, Rank.king) ])
        if x and x in hand:
            return x
    else:
        x = find_card_in_legal_moves(state, [Card(Suit.spades, Rank.queen), Card(Suit.spades, Rank.ace), Card(Suit.spades, Rank.king),
                              Card(Suit.hearts, Rank.ace), Card(Suit.hearts, Rank.king),
                              Card(Suit.clubs, Rank.ace), Card(Suit.diamonds, Rank.ace),
                              Card(Suit.clubs, Rank.king), Card(Suit.diamonds, Rank.king)])
        if x and x in hand:
            return x

    counts = suit_counts(state)
    for i, n in enumerate(counts):
        if n == 1:
            x = max_suit(state, LST[i] )
            if x and x in hand:
                return x

    x = find_card_in_legal_moves(state, [Card(Suit.hearts, Rank.queen), Card(Suit.hearts, Rank.jack), Card(Suit.hearts, Rank.ten),
                            Card(Suit.clubs, Rank.queen), Card(Suit.diamonds, Rank.queen),
                            Card(Suit.clubs, Rank.jack), Card(Suit.diamonds, Rank.jack), Card(Suit.spades, Rank.jack),
                            Card(Suit.clubs, Rank.ten), Card(Suit.diamonds, Rank.ten), Card(Suit.spades, Rank.ten)])
    if x and x in hand:
        return x
        
    for i, n in enumerate(counts):
        if n == 2:
            x = max_suit(state, LST[i] )
            if x and x in hand:
                return x
    
    x = max_suit(state, Suit.hearts)
    if x and x in hand:
        return x

    return max_card(state)

def default_follower(state):
            
    x = find_card_in_legal_moves(state, [Card(Suit.hearts, Rank.two),Card(Suit.hearts, Rank.three),Card(Suit.hearts, Rank.four)])
    if x:
        return x

    if (state.leader_idx + 3) % 4 != state.turn_idx:
        x = find_card_in_legal_moves(state, [Card(Suit.hearts, Rank.five)])
        if x:
            return x    

    
    x = max_safe_hand(state)
    if x:
        return x

    if state.turn_idx == (state.leader_idx + 3) % 4:
        x = max_excl_qs(state)
        if x:
            return x
        return max_card(state)
    else:
        x = min_excl_qs(state)
        if x:
            return x
        return min_card(state)
    
class MoreComplexPlayer_noSTM(Player):
    def __init__(self):
        pass

    def __str__(self):
        return "Complex Heuristic Player, No Cheating or Shooting the Moon"

    def play_card(self,game):
        return self.__call__(game.state)

    def __call__(self, state):
        KV = getKnownVoid(state)
        KV_Clubs = any([KV[0][i] for i in range(4)])
        KV_Diamonds = any([KV[1][i] for i in range(4)])
        KV_Spades = any([KV[3][i] for i in range(4)])
        SC = suit_counts(state)
        RC = rounds_counts(state)

        if state.leader_idx == state.turn_idx:

            if SC[0] <= SC[1]:
                if not KV_Clubs and RC[0] < 2 and SC[0] > 0:
                    x = max_suit(state, Suit.clubs)
                    if x:
                        return x
                elif not KV_Diamonds and RC[1] < 2 and SC[1] > 0:
                    x = max_suit(state, Suit.diamonds)
                    if x:
                        return x
            else:
                if not KV_Diamonds and RC[1] < 2 and SC[1] > 0:
                    x = max_suit(state, Suit.diamonds)
                    if x:
                        return x
                elif not KV_Clubs and RC[0] < 2 and SC[0] > 0:
                    x = max_suit(state, Suit.clubs)
                    if x:
                        return x

            if not check_QS_gone(state):
                if not find_card(state, [Card(Suit.spades, Rank.ace), Card(Suit.spades, Rank.king), Card(Suit.spades, Rank.queen)]) and not KV_Spades:
                    x = provoke_spades(state)
                    if x:
                        return x
            else:
                if not KV_Spades and RC[3] < 2 and SC[3] > 0:
                    x = max_suit(state, Suit.spades)
                    if x:
                        return x

            return default_low_card(state)
        else:
            if len([c for c in state.player_hands[state.turn_idx] if c.suit == state.suit]) == 0:
                return dispose_card(state)

            if sum([c.card_points() for c in state.trick if c]) == 0 and state.turn_idx == ((state.leader_idx + 3) %4):
                x = max_excl_qs(state)
                if x:
                    return x

            if state.suit == Suit.clubs and not KV_Clubs and RC[0] < 2 and SC[0] > 0:
                x = max_suit(state, Suit.clubs)
                if x:
                    return x
            if state.suit == Suit.diamonds and not KV_Diamonds and RC[1] < 2 and SC[1] > 0:
                x = max_suit(state, Suit.diamonds)
                if x:
                    return x
            if state.suit == Suit.spades and find_card(state, [Card(Suit.spades, Rank.queen)]):
                x = max_safe_hand(state)
                if x and x != Card(Suit.spades, Rank.queen):
                    return x
            if state.suit == Suit.spades and not KV_Spades and RC[3] < 2 and SC[3] > 0:
                x = provoke_spades(state)
                if x:
                    return x

            return default_follower(state)

def opponent_suit_count(state):
    """Checks for opponent void (cheating)"""
    lst = list()
    for i in range(4):
        count = [0,0,0,0]
        for card in state.player_hands[i]:
            count[card.suit.value] += 1
        lst.append(count)
    return lst

def opponent_has_points(state):
    """Checks for opponent having points (cheating)"""
    lst = [False,False,False,False]
    for i in range(4):
        for card in state.player_hands[i]:
            if card.qs() or card.h():
                lst[i] = True
    return lst

def check_opp_void_or_has_no_points(state, suit):
    OHP = opponent_has_points(state)
    OSC = opponent_suit_count(state)

    for i in range(4):
        if i != state.turn_idx:
            if OHP[i] and OSC[i][suit.value] == 0:
                return False
    return True

def playersbehind_check_opp_void_or_has_no_points(state):
    OHP = opponent_has_points(state)
    OSC = opponent_suit_count(state)

    for i in range(4):
        if i != state.turn_idx and state.trick[i] is None:
            if OHP[i] and OSC[i][state.suit.value] == 0:
                return False
    return True    

def playersbehind_check_qs(state):
    for i in range(4):
        if i != state.turn_idx and state.trick[i] is None:
            for card in state.player_hands[i]:
                if card.qs():
                    return True
    return False

def max_safe_hand_cheating(state):
    if state.suit == None:
        raise ValueError("This cannot be calculated if we are at the leader")

    m = max([t for t in state.trick if t and t.suit == state.suit])
    
    next_player = (state.turn_idx + 1) % 4
    next_next_player = (state.turn_idx + 2) % 4

    if state.trick[next_player] is None:
        tmp = min([t for t in state.player_hands[next_player] if t and t.suit == state.suit], default = None)
        if tmp is not None:
            m = max(tmp, m)
    if state.trick[next_next_player] is None:
        tmp = min([t for t in state.player_hands[next_next_player] if t and t.suit == state.suit], default = None)
        if tmp is not None:
            m = max(tmp, m)

    safe_hands = [t for t in state.legal_moves() if t.rank < m.rank]
    if safe_hands == None:
        return None
    else:
        return max(safe_hands, default = None, key = lambda c : c.rank)

class ComplexCheatingPlayer_noSTM(Player):
    def __init__(self):
        pass

    def __str__(self):
        return "Complex Heuristic Player, with Cheating and No Shooting the Moon"

    def play_card(self,game):
        return self.__call__(game.state)

    def __call__(self, state):
        SC = suit_counts(state)

        if state.leader_idx == state.turn_idx:

            if SC[0] <= SC[1]:
                if check_opp_void_or_has_no_points(state, Suit.clubs) and SC[0] > 0:
                    x = max_suit(state, Suit.clubs)
                    if x:
                        return x
                elif check_opp_void_or_has_no_points(state, Suit.diamonds) and SC[1] > 0:
                    x = max_suit(state, Suit.diamonds)
                    if x:
                        return x
            else:
                if check_opp_void_or_has_no_points(state, Suit.diamonds) and SC[1] > 0:
                    x = max_suit(state, Suit.diamonds)
                    if x:
                        return x
                elif check_opp_void_or_has_no_points(state, Suit.clubs) and SC[0] > 0:
                    x = max_suit(state, Suit.clubs)
                    if x:
                        return x

            if not check_QS_gone(state):
                if not find_card(state, [Card(Suit.spades, Rank.ace), Card(Suit.spades, Rank.king), Card(Suit.spades, Rank.queen)]) and check_opp_void_or_has_no_points(state, Suit.spades):
                    x = provoke_spades(state)
                    if x:
                        return x
            else:
                if check_opp_void_or_has_no_points(state, Suit.spades) and SC[3] > 0:
                    x = max_suit(state, Suit.spades)
                    if x:
                        return x

            for suit in LST:
                if check_opp_void_or_has_no_points(state, suit):
                    x = min_suit(state, suit)
                    if x and x.suit == Suit.spades and x.rank.value > Rank.queen.value:
                        if not playersbehind_check_qs(state):
                            return x
                    else:
                        if x and not x.qs() and not x.h():
                            return x

            return default_low_card(state)
        else:
            if len([c for c in state.player_hands[state.turn_idx] if c.suit == state.suit]) == 0:
                return dispose_card(state)

            if max_safe_hand_cheating(state) and max_safe_hand_cheating(state).rank.value >= dispose_card(state).rank.value:
                return dispose_card(state)

            if sum([c.card_points() for c in state.trick if c]) == 0 and playersbehind_check_opp_void_or_has_no_points(state):
                if state.suit != Suit.spades:  #if clubs or diamonds, you are safe. If hearts, you will never get here
                    x = max_excl_qs(state)
                    if x:
                        return x
                else:
                    if not playersbehind_check_qs(state):
                        x = max_excl_qs(state)
                        if x:
                            return x
                    else:
                        x = provoke_spades(state)
                        if x:
                            return x


            x = max_safe_hand_cheating(state)
            if x:
                return x

            return default_follower(state)                

