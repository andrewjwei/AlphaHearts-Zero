import random
import multiprocessing
import functools

class PIMC:
    """
    A PIMC object is a function that once given a state will make a move based on that state.
    To initialize the object, one must give it a sampleModule and a PerfInfoValue.
    The sampleModule will determine the method of determinization. The variable n will indicate how many determinizations.
    The PerfInfoValue will determine the value of each perfect information state.
    """
    def __init__(self, sampleModule, PerfInfoValue, n = 100, multiprocessing = False):
        """
        A PIMC object is a function that once given a state will make a move based on that state.
        To initialize the object, one must give it a sampleModule and a PerfInfoValue.
        The sampleModule will determine the method of determinization. The variable n will indicate how many determinizations.
        The PerfInfoValue will determine the value of each perfect information state.
        """
        self.sampleModule = sampleModule
        self.PerfInfoValue = PerfInfoValue
        self.n = n
        self.multiprocessing = multiprocessing

    def set_n(self,n):
        self.n = n

    def _iterate(self, sampleModule, moves):
        x = sampleModule()
        self.PerfInfoValue.precompute_state(x)
        return [self.PerfInfoValue(x,m) for m in moves]

    def __call__(self, state):
                
        moves = state.legal_moves()
        val = [0 for _ in moves]
        sampleModule = self.sampleModule(state)

        if self.multiprocessing:
            with multiprocessing.Pool(self.n) as p:
                rewards = p.map(functools.partial(self._iterate, sampleModule), [moves for _ in range(self.n)])
            for r in rewards:
                val = [val[i] + r[i] for i in range(len(moves))]
        else:
            for _ in range(self.n):
                x = sampleModule()
                self.PerfInfoValue.precompute_state(x)
                for i, m in enumerate(moves):
                    val[i] += self.PerfInfoValue(x,m)        
        
        most_val = -float('inf')
        best_m = [moves[0]]
        for i, m in enumerate(moves):
            if val[i] > most_val:
                most_val = val[i]
                best_m = [m]
            elif val[i] == most_val:
                best_m.append(m)
                
        return random.choice(best_m)

