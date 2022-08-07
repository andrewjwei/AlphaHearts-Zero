

class AbstractPerfInfoModule:
    """
    A Perfect Information Module must calculate the perfect information value of a state, for use in the PIMC algorithm.
    The PerfInfoModule may be initiated any way that the user wants. However, it must satisfy the following constraints.
    """

    def precompute_state(self,state):
        """In certain cases, the PerfInfoModule may precompute the state. This must be implemented, even as "pass" """
        raise NotImplementedError

    def __str__(self):
        return NotImplementedError

    def __call__(self, state, action):
        """This function must return the value of any state, action pairing."""
        raise NotImplementedError