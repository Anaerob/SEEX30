import numpy as np

import Constants as c
import Trainer


class Game:
    
    
    def __init__(self, blackTeam, whiteTeam, state=None):
        
        # Constants
        self.blackTeam = blackTeam
        self.whiteTeam = whiteTeam
        
        # State [Black, White]
        self.round = 0
        self.running = True
        self.win = [False, False]
        self.trainers = [
            Trainer.Trainer('Black', blackTeam),
            Trainer.Trainer('White', whiteTeam)]
        if state is not None:
            self.setState(state)
    
    def setState(self, state):
        
        # Set the game to a specific state
        self.round = state[0]
        self.running = state[1]
        self.win = [state[2], state[3]]
        self.trainers = [
            Trainer.Trainer('Black', self.blackTeam, state[4]),
            Trainer.Trainer('White', self.whiteTeam, state[5])]
  
    def getState(self, isBlack):
        
        # Returns the complete state of the game
        tempState = []
        tempState.append(self.round)
        tempState.append(self.running)
        p = 1
        if isBlack:
            p = 0
        tempState.append(self.win[p])
        tempState.append(self.win[(p + 1) % 2])
        tempState.append(self.trainers[p].getState())
        tempState.append(self.trainers[(p + 1) % 2].getState())
        return tempState
    
    def getFeatures(self, isBlack):
        
        # Returns the inputs for the neural network AI
        tempFeatures = np.array([])
        p = 1
        if isBlack:
            p = 0
        tempFeatures = np.append(tempFeatures, self.trainers[p].getFeatures())
        tempFeatures = np.append(tempFeatures, self.trainers[(p + 1) % 2].getFeatures())
        return tempFeatures
    
    def progress(self):
        
        # Make sure every action choice is legal
        for iT in range(2):
            if not self.trainers[iT].nextActionSet:
                exit('[Game.progress()]: Trainer ' + self.trainers[iT].name + ' move not set!')
            elif self.trainers[iT].nextAction < 1 or self.trainers[iT].nextAction > 2:
                exit('[Game.progress()]: Trainer ' + self.trainers[iT].name + ' chosen move is illegal!')
            elif self.trainers[iT].pokemon.moves[self.trainers[iT].nextAction - 1].cPP <= 0:
                exit('[Game.progress()]: Trainer ' + self.trainers[iT].name + ' chose move with no PP remaining!')
        
        # Determine who strikes first based on speed
        t = 0
        if self.trainers[0].pokemon.speed < self.trainers[1].pokemon.speed:
            t = 1
        elif self.trainers[0].pokemon.speed == self.trainers[1].pokemon.speed:
            t = np.random.randint(2)
        
        # Use moves in order, only use second move if Pokemon still active
        self.useMove(t)
        self.trainers[t].resetNextAction()
        if self.trainers[(t + 1) % 2].pokemon.cHP > 0:
            self.useMove((t + 1) % 2)
            self.trainers[(t + 1) % 2].resetNextAction()
        
        # Check if either pokemon fainted, proclaim victor
        for iT in range(2):
            if self.trainers[iT].pokemon.cHP <= 0:
                self.running = False
                self.win[(iT + 1) % 2] = True
        
        self.round += 1
    
    def useMove(self, t):
        
        self.trainers[t].pokemon.moves[self.trainers[t].nextAction - 1].cPP -= 1
        
        # Check if move misses (correctly implements the 1/256 miss bug)
        if np.random.randint(256) < self.trainers[t].pokemon.moves[self.trainers[t].nextAction - 1].accuracy:
            
            # Damaging move: calculate and deduct damage
            if self.trainers[t].pokemon.moves[self.trainers[t].nextAction - 1].power != 0:
                
                # Critical hit: calculate damage with double level and no modifiers
                if np.random.randint(256) < np.floor(self.trainers[t].pokemon.baseSpeed / 2):
                    damage = self.calculateDamage(
                        2 * self.trainers[t].pokemon.level,
                        self.trainers[t].pokemon.attack,
                        self.trainers[t].pokemon.moves[self.trainers[t].nextAction - 1].power,
                        self.trainers[(t + 1) % 2].pokemon.defense)
                else:
                    
                    # Normal calculation with modifiers
                    damage = self.calculateDamage(
                        self.trainers[t].pokemon.level,
                        np.floor(
                            c.statMods[self.trainers[t].modAttack]
                            * self.trainers[t].pokemon.attack / 100),
                        self.trainers[t].pokemon.moves[self.trainers[t].nextAction - 1].power,
                        np.floor(
                            c.statMods[self.trainers[(t + 1) % 2].modDefense]
                            * self.trainers[(t + 1) % 2].pokemon.defense / 100))
                
                self.trainers[(t + 1) % 2].pokemon.cHP -= int(damage)
            
            # Stat modifying move: modify the stat
            if self.trainers[t].pokemon.moves[self.trainers[t].nextAction - 1].modChance != 0:
                if self.trainers[t].pokemon.moves[self.trainers[t].nextAction - 1].modAttack < 0:
                    if self.trainers[(t + 1) % 2].modAttack > 0:
                        self.trainers[(t + 1) % 2].modAttack -= 1
                elif self.trainers[t].pokemon.moves[self.trainers[t].nextAction - 1].modDefense < 0:
                    if self.trainers[(t + 1) % 2].modDefense > 0:
                        self.trainers[(t + 1) % 2].modDefense -= 1
    
    def calculateDamage(self, level, attack, power, defense):
        
        # Calculate raw damage
        factor1 = 2 + np.floor(2 * level / 5)
        factor2 = power * attack
        denominator = 50 * defense
        unmodified = 2 + np.floor(factor1 * factor2 / denominator)
        
        # Apply random modifier
        rand = np.random.randint(217, 256)
        damage = np.floor(unmodified * rand / 255)
        
        return int(damage)

#