import numpy as np

import Constants as c
import Game


class AI:
    
    
    def getAction(self, state):
        
        sim = Game.Game(False, state)
        if sim.forceSwitch[0]:
            action = self.getSwitch(state)
        else:
            moves = [7, 8, 9, 10]
            for iM in range(1, 5):
                if sim.trainers[0].pokemon[sim.trainers[0].cP].moves[iM].cPP <= 0:
                    moves.remove(iM + 6)
            if len(moves) == 0:
                action = [0, 0]
            else:
                choice = np.random.choice(moves)
                action = list(c.actions[choice])
        return action
        
    def getSwitch(self, state):
        
        sim = Game.Game(False, state)
        switches = [1, 2, 3, 4, 5, 6]
        for iP in range(1, 7):
            if sim.trainers[0].pokemon[iP].cHP <= 0:
                switches.remove(iP)
            elif sim.trainers[0].cP == iP:
                switches.remove(iP)
        choice = np.random.choice(switches)
        switch = list(c.actions[choice])
        return switch

#