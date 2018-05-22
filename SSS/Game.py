import numpy as np


class Game:
    
    
    def __init__(self, state=None):
        
        # Constants
        self.n = 5
        self.goal = self.n ** 2
        self.softLimit = self.goal - 1
        
        # State [Black, White]
        self.round = 0
        self.running = True
        self.multiplier = [1, 1]
        self.points = [0, 0]
        self.win = [False, False]
        if state is not None:
            self.setState(state)
    
    def setState(self, state):
        
        # Set the game to a specific state
        self.round = state[0]
        self.running = state[1]
        self.multiplier = [state[2], state[3]]
        self.points = [state[4], state[5]]
        self.win = [state[6], state[7]]
    
    def getState(self, isBlack):
        
        # Returns the complete state of the game
        tempState = []
        tempState.append(self.round)
        tempState.append(self.running)
        p = 1
        if isBlack:
            p = 0
        tempState.append(self.multiplier[p])
        tempState.append(self.multiplier[(p + 1) % 2])
        tempState.append(self.points[p])
        tempState.append(self.points[(p + 1) % 2])
        tempState.append(self.win[p])
        tempState.append(self.win[(p + 1) % 2])
        return tempState
    
    def getFeatures(self, isBlack):
        
        # Returns the two inputs for the neural network AI
        tempFeatures = np.array([])
        p = 1
        if isBlack:
            p = 0
        tempFeatures = np.append(
            tempFeatures, (self.goal - self.points[p]) / self.goal)
        tempFeatures = np.append(
            tempFeatures,
            (1 + (self.multiplier[p] <= self.softLimit)
                * ((self.multiplier[p] - 1) / self.softLimit - 1)))
        return tempFeatures
    
    def progress(self, actions):
        
        # Carry out both players actions in random order
        p = np.random.randint(2)
        self.doAction(actions[p], p)
        if self.points[p] < self.goal:
            self.doAction(actions[(p + 1) % 2], (p + 1) % 2)
        
        # Check if any player won the game
        for iP in range(2):
            if self.points[iP] >= self.goal:
                self.running = False
                self.win[iP] = True
        
        self.round += 1
    
    def doAction(self, action, p):
        
        # Increase the multiplier
        if action == 0:
            if self.multiplier[p] <= self.softLimit:
                self.multiplier[p] += 1
            else:
                self.points[p] += self.multiplier[p]
        
        # Increase the points
        elif action == 1:
            self.points[p] += self.multiplier[p]

#