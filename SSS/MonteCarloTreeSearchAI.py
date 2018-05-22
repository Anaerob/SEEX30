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
        
        # Initialize and start the search
        actions = [0, 1]
        bStrategyTries = {}
        bStrategyWins = {}
        wStrategyTries = {}
        wStrategyWins = {}
        for iSearch in range(self.search):
            
            # Initialize and play the simulated game
            sim = Game.Game(state)
            simStart = sim.round
            bTryingNow = ''
            wTryingNow = ''
            while sim.running:
                
                # Don't search past the specified depth level
                if sim.round - simStart >= self.depth:
                    sim.progress([np.random.randint(2), np.random.randint(2)])
                else:
                    
                    # Construct the action value function Q for both players
                    bQ = np.array([])
                    wQ = np.array([])
                    for iAction in range(2):
                        bTryTemp = bTryingNow
                        bTryTemp += str(iAction)
                        wTryTemp = wTryingNow
                        wTryTemp += str(iAction)
                        
                        # Q for an action is the simulated win percentage
                        if bTryTemp in bStrategyTries:
                            bQ = np.append(
                                bQ,
                                (bStrategyWins[bTryTemp]
                                    / bStrategyTries[bTryTemp]))
                        
                        # Always prefer untried strategies
                        else:
                            bQ = np.append(bQ, self.almostGuaranteed)
                        
                        if wTryTemp in wStrategyTries:
                            wQ = np.append(
                                wQ,
                                (wStrategyWins[wTryTemp]
                                    / wStrategyTries[wTryTemp]))
                        else:
                            wQ = np.append(wQ, self.almostGuaranteed)
                    
                    # With a small probability epsilon:
                    # Choose action uniformly randomly
                    if np.random.random() < self.epsilon:
                        bQ = np.ones(2)
                    if np.random.random() < self.epsilon:
                        wQ = np.ones(2)
                    
                    # If the specified temperature is too low,
                    # choose the action with maximum Q
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
                        
                        # Choose action using a probabilistic softmax
                        bPolicy = (np.exp(bQ / self.temperature)
                            / np.sum(np.exp(bQ / self.temperature), axis = 0))
                        bChoice = np.random.choice(actions, p = bPolicy)
                        wPolicy = (np.exp(wQ / self.temperature)
                            / np.sum(np.exp(wQ / self.temperature), axis = 0))
                        wChoice = np.random.choice(actions, p = wPolicy)
                    
                    # Progress the simulation
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
        
        # Based on the results of the simulations,
        # choose the action resulting in the highest probability of winning
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