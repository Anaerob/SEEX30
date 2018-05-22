import numpy as np

import Constants as c
import Move


class Pokemon:
    
    
    def __init__(self, index, state = None):
        
        # Constants
        self.index = index
        self.name = c.PN[index]
        self.HP = c.PS[index][0]
        self.attack = c.PS[index][1]
        self.defense = c.PS[index][2]
        self.special = c.PS[index][3]
        self.speed = c.PS[index][4]
        self.baseSpeed = c.PBS[index][4]
        
        # State
        self.cHP = c.PS[index][0]
        self.frozen = False
        self.paralyzed = False
        self.sleeping = 0
        self.moves = [Move.Move(165)]
        for iM in range(4):
            self.moves.append(Move.Move(c.PM[index][iM]))
        if state is not None:
            self.setState(state)
    
    def setState(self, state):
        
        self.cHP = state[0]
        self.frozen = state[1]
        self.paralyzed = state[2]
        self.sleeping = state[3]
        self.moves = [Move.Move(165)]
        for iM in range(4):
            self.moves.append(Move.Move(c.PM[self.index][iM], state[4 + iM]))
    
    def getState(self):
        
        tempState = []
        tempState.append(self.cHP)
        tempState.append(self.frozen)
        tempState.append(self.paralyzed)
        tempState.append(self.sleeping)
        for iM in range(4):
            tempState.append(self.moves[iM + 1].getState())
        return tempState
    
    def getFeatures(self):
        
        tempFeatures = np.array([])
        tempFeatures = np.append(tempFeatures, self.cHP / c.PS[self.index][0])
        return tempFeatures

#