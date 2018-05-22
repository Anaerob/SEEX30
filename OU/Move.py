import numpy as np

import Constants as c


class Move:
    
    
    def __init__(self, index, state=None):
        
        # Constants
        self.index = index
        self.name = c.MN[index]
        self.accuracy = c.MS[index][1]
        self.PP = c.MS[index][2]
        
        # State
        self.cPP = c.MS[index][2]
        
        if state is not None:
            self.setState(state)
    
    def setState(self, state):
        self.cPP = state
    
    def getState(self):
        return self.cPP
    
    def getFeatures(self):
        return np.array([(self.cPP < 4) * (1 - self.cPP / 4)])

#