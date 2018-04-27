import numpy as np

import Constants as c
import Move


class Pokemon:
    
    
    def __init__(self, index, state=None):
        
        # Constants
        self.index = index
        self.name = c.PN[index]
        self.level = 5
        self.baseSpeed = c.PBS[index][4]
        self.attack = c.PS[index][1]
        self.defense = c.PS[index][2]
        self.speed = c.PS[index][4]
        
        # State
        self.cHP = c.PS[index][0]
        self.moves = [Move.Move(c.PM[index][0]), Move.Move(c.PM[index][1])]
        if state is not None:
            self.setState(state)
    
    def setState(self, state):
        
        self.cHP = state[0]
        self.moves = [
            Move.Move(c.PM[self.index][0], state[1]),
            Move.Move(c.PM[self.index][1], state[2])]
    
    def getState(self):
        
        tempState = []
        tempState.append(self.cHP)
        tempState.append(self.moves[0].getState())
        tempState.append(self.moves[1].getState())
        return tempState
    
    def getFeatures(self):
        
        tempFeatures = np.array([])
        tempFeatures = np.append(tempFeatures, self.cHP / c.PS[self.index][0])
        tempFeatures = np.append(tempFeatures, self.moves[0].getFeatures())
        tempFeatures = np.append(tempFeatures, self.moves[1].getFeatures())
        return tempFeatures

#