import numpy as np

import Constants as c
import Pokemon


class Trainer:
    
    
    def __init__(self, name, team, state=None):
        
        # Constants
        self.name = name
        self.team = team
        
        # State
        self.modAttack = 6
        self.modDefense = 6
        self.nextAction = 0
        self.nextActionSet = False
        self.pokemon = Pokemon.Pokemon(team)
        if state is not None:
            self.setState(state)
    
    def setNextAction(self, action):
        
        if self.nextActionSet:
            exit('[Trainer.setNextMove()]: ' + self.name + ' move already set!')
        if action < 1 or action > 2:
            exit('[Trainer.setNextMove()]: Illegal move set by ' + self.name + '!')
        self.nextAction = action
        self.nextActionSet = True
    
    def setState(self, state):
        
        self.modAttack = state[0]
        self.modDefense = state[1]
        self.nextAction = state[2]
        self.nextActionSet = state[3]
        self.pokemon = Pokemon.Pokemon(self.team, state[4])
    
    def getState(self):
        
        tempState = []
        tempState.append(self.modAttack)
        tempState.append(self.modDefense)
        tempState.append(self.nextAction)
        tempState.append(self.nextActionSet)
        tempState.append(self.pokemon.getState())
        return tempState
    
    def getFeatures(self):
        
        tempFeatures = np.array([])
        tempFeatures = np.append(tempFeatures, 1 - self.modAttack / 6)
        tempFeatures = np.append(tempFeatures, 1 - self.modDefense / 6)
        tempFeatures = np.append(tempFeatures, self.pokemon.getFeatures())
        return tempFeatures
    
    def resetNextAction(self):
        
        self.nextActionSet = False
        self.nextAction = 0

#