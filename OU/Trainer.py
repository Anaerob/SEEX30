import numpy as np

import Constants as c
import Pokemon


class Trainer:
    
    
    def __init__(self, name, state = None):
        
        # Constants
        self.name = name
        
        # State
        self.cP = 1
        self.rP = 6
        self.nextActionSet = False
        self.nextAction = list(c.actions[0])
        self.recharge = False
        self.substitute = 0
        self.specialMod = 6
        self.speedMod = 6
        self.pokemon = [Pokemon.Pokemon(0)]
        for iP in range(6):
            self.pokemon.append(Pokemon.Pokemon(c.team[iP]))
        if state is not None:
            self.setState(state)
    
    def setNextAction(self, action):
        
        if self.nextActionSet:
            exit('[Trainer.setNextAction()]: ' + self.name + ' action already set!')
        if action[0] < 0 or action[0] > 6:
            exit('[Trainer.setNextAction()]: Illegal switch set by Trainer ' + self.name + '!')
        if action[1] < 0 or action[1] > 4:
            exit('[Trainer.setNextAction()]: Illegal move set by Trainer ' + self.name + '!')
        self.nextAction = action
        self.nextActionSet = True
    
    def setState(self, state):
        
        self.cP = state[0]
        self.rP = state[1]
        self.nextActionSet = state[2]
        self.nextAction = state[3]
        self.recharge = state[4]
        self.substitute = state[5]
        self.specialMod = state[6]
        self.speedMod = state[7]
        self.pokemon = [Pokemon.Pokemon(0)]
        for iP in range(6):
            self.pokemon.append(Pokemon.Pokemon(c.team[iP], state[8 + iP]))
    
    def getState(self):
        
        tempState = []
        tempState.append(self.cP)
        tempState.append(self.rP)
        tempState.append(self.nextActionSet)
        tempState.append(self.nextAction)
        tempState.append(self.recharge)
        tempState.append(self.substitute)
        tempState.append(self.specialMod)
        tempState.append(self.speedMod)
        for iP in range(6):
            tempState.append(self.pokemon[iP + 1].getState())
        return tempState
    
    def getFeatures(self):
        
        tempFeatures = np.array([])
        tempFeatures = np.append(tempFeatures, self.cP / 6)
        return tempFeatures
    
    def healDamage(self, damage):
        
        self.pokemon[self.cP].cHP += damage
        if self.pokemon[self.cP].cHP > self.pokemon[self.cP].HP:
            healed = damage - (self.pokemon[self.cP].cHP - self.pokemon[self.cP].HP)
            self.pokemon[self.cP].cHP = self.pokemon[self.cP].HP
        else:
            healed = damage
        return damage
    
    def inflictDamage(self, damage, ignoreSub): # ADD IGNORE SUBSTITUTE INPUT?
        
        overkill = 0
        subBroke = False
        if self.substitute <= 0 or ignoreSub:
            if self.pokemon[self.cP].cHP > damage:
                self.pokemon[self.cP].cHP -= damage
            else:
                overkill = damage - self.pokemon[self.cP].cHP
                self.pokemon[self.cP].cHP = 0
        else:
            if self.substitute <= damage:
                overkill = damage - self.substitute
                self.substitute = 0
                subBroke = True
            else:
                self.substitute -= damage
        return [overkill, subBroke]
    
    def resetNextAction(self):
        
        self.nextActionSet = False
        self.nextAction = list(c.actions[0])

#