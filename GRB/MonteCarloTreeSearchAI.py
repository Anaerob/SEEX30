import numpy as np

import Game
import Constants as c


class AI:
    
    
    def __init__(self, bT, wT, d, e, s, t):
        
        self.blackTeam = bT
        self.whiteTeam = wT
        self.almostGuaranteed = 1 + 10 * t
        self.depth = d
        self.epsilon = e
        self.search = s
        self.temperature = t
    
    def getAction(self, state):
        
        bStrategyTries = {}
        bStrategyWins = {}
        wStrategyTries = {}
        wStrategyWins = {}
        for iSearch in range(self.nSearch):
            
            # Initialize a simulation starting from the given state
            sim = Game.Game(self.blackTeam, self.whiteTeam, state)
            simStart = sim.round
            bTryingNow = ''
            wTryingNow = ''
            while sim.running:
                bActions = list(c.actions)
                if sim.trainers[0].pokemon.moves[1].cPP <= 0:
                    bActions.remove(2)
                wActions = list(c.actions)
                if sim.trainers[1].pokemon.moves[1].cPP <= 0:
                    wActions.remove(2)
                if sim.round - simStart >= self.depth:
                    sim.trainers[0].setNextAction(np.random.choice(bActions))
                    sim.trainers[1].setNextAction(np.random.choice(wActions))
                    sim.progress()
                else:
                    
                    # Build Q by checking tree
                    bQ = np.array([])
                    for iAction in range(len(bActions)):
                        bTryTemp = bTryingNow
                        bTryTemp += str(bActions[iAction])
                        if bTryTemp in bStrategyTries:
                            bQ = np.append(bQ, bStrategyWins[bTryTemp] / bStrategyTries[bTryTemp])
                        else:
                            bQ = np.append(bQ, self.almostGuaranteed)
                    wQ = np.array([])
                    for iAction in range(len(wActions)):
                        wTryTemp = wTryingNow
                        wTryTemp += str(wActions[iAction])
                        if wTryTemp in wStrategyTries:
                            wQ = np.append(wQ, wStrategyWins[wTryTemp] / wStrategyTries[wTryTemp])
                        else:
                            wQ = np.append(wQ, self.almostGuaranteed)
                    
                    # With some probability epsilon: choose uniformly randomly
                    if np.random.random() < self.epsilon:
                        bQ = np.ones(len(bActions))
                    if np.random.random() < self.epsilon:
                        wQ = np.ones(len(wActions))
                    
                    # Choose action using softmax unless temperature is too low
                    if self.temperature < 0.01:
                        if bQ.tolist().count(max(bQ)) != 1:
                            print('bQ[0] = bQ[1] in search')
                        bChoice = bQ.tolist().index(max(bQ))
                        if wQ.tolist().count(max(wQ)) != 1:
                            print('wQ[0] = wQ[1] in search')
                        wChoice = wQ.tolist().index(max(wQ))
                    else:
                        bPolicy = np.exp(bQ / self.temperature) / np.sum(np.exp(bQ / self.temperature), axis = 0)
                        bChoice = np.random.choice(c.actions, p = bPolicy)
                        wPolicy = np.exp(wQ / self.temperature) / np.sum(np.exp(wQ / self.temperature), axis = 0)
                        wChoice = np.random.choice(c.actions, p = wPolicy)
                    bTryingNow += str(bChoice)
                    wTryingNow += str(wChoice)
                    sim.trainers[0].setNextAction(bChoice)
                    sim.trainers[1].setNextAction(wChoice)
                    sim.progress()
            
            # Update and extend the search tree
            for subStrategy in range(
                    1, min(sim.round - simStart, self.depth) + 1):
                if bTryingNow[0:subStrategy] in bStrategyTries:
                    bStrategyTries[bTryingNow[0:subStrategy]] += 1
                    if sim.win[0]:
                        bStrategyWins[bTryingNow[0:subStrategy]] += 1
                else:
                    bStrategyTries[bTryingNow[0:subStrategy]] = 1
                    if sim.win[0]:
                        bStrategyWins[bTryingNow[0:subStrategy]] = 1
                    else:
                        bStrategyWins[bTryingNow[0:subStrategy]] = 0
                    break
            for subStrategy in range(
                    1, min(sim.round - simStart, self.depth) + 1):
                if wTryingNow[0:subStrategy] in wStrategyTries:
                    wStrategyTries[wTryingNow[0:subStrategy]] += 1
                    if sim.win[1]:
                        wStrategyWins[wTryingNow[0:subStrategy]] += 1
                else:
                    wStrategyTries[wTryingNow[0:subStrategy]] = 1
                    if sim.win[1]:
                        wStrategyWins[wTryingNow[0:subStrategy]] = 1
                    else:
                        wStrategyWins[wTryingNow[0:subStrategy]] = 0
                    break
        
        # Build final Q from the results of the tree search
        sim = Game.Game(self.blackTeam, self.whiteTeam, state)
        actions = list(c.actions)
        if sim.trainers[0].pokemon.moves[1].cPP <= 0:
            actions.remove(2)
        Q = np.array([])
        for iAction in range(len(actions)):
            Q = np.append(Q, bStrategyWins[str(actions[iAction])] / bStrategyTries[str(actions[iAction])])
        
        if Q.tolist().count(max(Q)) != 1:
            print('Q[0] = Q[1] in final')
        choice = Q.tolist().index(max(Q))
        return choice

#