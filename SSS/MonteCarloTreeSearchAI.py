import numpy as np

import Game


class AI:
    
    
    def __init__(self, d, e, s, t):
        
        self.almostGuaranteed = 1 + 10 * t
        self.depth = d
        self.epsilon = e
        self.search = s
        self.temperature = t
    
    def getAction(self, state):
        
        actions = [0, 1]
        bStrategyTries = {}
        bStrategyWins = {}
        wStrategyTries = {}
        wStrategyWins = {}
        
        for iSearch in range(self.search):
            sim = Game.Game(state)
            simStart = sim.round
            bTryingNow = ''
            wTryingNow = ''
            
            while sim.running:
                if sim.round - simStart >= self.depth:
                    sim.progress([np.random.randint(2), np.random.randint(2)])
                else:
                    bQ = np.array([])
                    wQ = np.array([])
                    
                    for iAction in range(2):
                        bTryTemp = bTryingNow
                        bTryTemp += str(iAction)
                        wTryTemp = wTryingNow
                        wTryTemp += str(iAction)
                        if bTryTemp in bStrategyTries:
                            bQ = np.append(
                                bQ,
                                (bStrategyWins[bTryTemp]
                                    / bStrategyTries[bTryTemp]))
                        else:
                            bQ = np.append(bQ, self.almostGuaranteed)
                        if wTryTemp in wStrategyTries:
                            wQ = np.append(
                                wQ,
                                (wStrategyWins[wTryTemp]
                                    / wStrategyTries[wTryTemp]))
                        else:
                            wQ = np.append(wQ, self.almostGuaranteed)
                    
                    # Choose action uniformly randomly with probability epsilon
                    if np.random.random() < self.epsilon:
                        bQ = np.ones(2)
                    if np.random.random() < self.epsilon:
                        wQ = np.ones(2)
                    
                    # Choose action using softmax unless temperature is too low
                    if self.temperature < 0.01:
                        if bQ[0] == bQ[1]:
                            bChoice = np.random.randint(2)
                        else:
                            bChoice = bQ.tolist().index(max(bQ))
                        if wQ[0] == wQ[1]:
                            wChoice = np.random.randint(2)
                        else:
                            wChoice = wQ.tolist().index(max(wQ))
                    else:
                        bPolicy = (np.exp(bQ / self.temperature)
                            / np.sum(np.exp(bQ / self.temperature), axis = 0))
                        bChoice = np.random.choice(actions, p = bPolicy)
                        wPolicy = (np.exp(wQ / self.temperature)
                            / np.sum(np.exp(wQ / self.temperature), axis = 0))
                        wChoice = np.random.choice(actions, p = wPolicy)
                    
                    bTryingNow += str(bChoice)
                    wTryingNow += str(wChoice)
                    sim.progress([bChoice, wChoice])
            
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
        
        Q = np.array([])
        for iAction in range(2):
            Q = np.append(
                Q,
                (bStrategyWins[str(iAction)] / bStrategyTries[str(iAction)]))
        if Q[0] == Q[1]:
            choice = np.random.randint(2)
        else:
            choice = Q.tolist().index(max(Q))
        return choice

#