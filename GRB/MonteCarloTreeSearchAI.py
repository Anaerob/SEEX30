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
        
        # Initialize and start the search
        bStrategyTries = {}
        bStrategyWins = {}
        wStrategyTries = {}
        wStrategyWins = {}
        for iSearch in range(self.search):
            
            # Initialize and play the simulated game from the given state
            sim = Game.Game(self.blackTeam, self.whiteTeam, state)
            for iT in range(2):
                sim.trainers[iT].resetNextAction()
            simStart = sim.round
            bTryingNow = ''
            wTryingNow = ''
            
            # Make sure all allowed actions are tried at least once
            bActions = list(c.actions)
            if sim.trainers[0].pokemon.moves[1].cPP <= 0:
                bActions.remove(2)
            wActions = list(c.actions)
            if sim.trainers[1].pokemon.moves[1].cPP <= 0:
                wActions.remove(2)
            bGuaranteedAction = 0
            wGuaranteedAction = 0
            for iAction in range(len(bActions)):
                if str(bActions[iAction]) not in bStrategyTries:
                    bGuaranteedAction = bActions[iAction]
                    break
            for iAction in range(len(wActions)):
                if str(wActions[iAction]) not in wStrategyTries:
                    wGuaranteedAction = wActions[iAction]
                    break
            
            while sim.running:
                
                # Make a list of all allowed actions
                bActions = list(c.actions)
                if sim.trainers[0].pokemon.moves[1].cPP <= 0:
                    bActions.remove(2)
                wActions = list(c.actions)
                if sim.trainers[1].pokemon.moves[1].cPP <= 0:
                    wActions.remove(2)
                
                # Don't search past the specified depth level
                if sim.round - simStart >= self.depth:
                    sim.trainers[0].setNextAction(np.random.choice(bActions))
                    sim.trainers[1].setNextAction(np.random.choice(wActions))
                    sim.progress()
                else:
                    
                    # Check for unplayed actions
                    if bGuaranteedAction != 0:
                        bChoice = bGuaranteedAction
                        bGuaranteedAction = 0
                    else:
                        
                        # Construct the action value function Q
                        if np.random.random() < self.epsilon:
                            
                            # Uniformly random
                            bQ = np.ones(len(bActions))
                        else:
                            
                            # Simulated win percentage thus far
                            bQ = np.array([])
                            for iAction in range(len(bActions)):
                                bTryTemp = bTryingNow
                                bTryTemp += str(bActions[iAction])
                                if bTryTemp in bStrategyTries:
                                    bQ = np.append(bQ, bStrategyWins[bTryTemp] / bStrategyTries[bTryTemp])
                                else:
                                    
                                    # Prefer untried strategies
                                    bQ = np.append(bQ, self.almostGuaranteed)
                        
                        # If the specified temperature is too low,
                        # choose the action with maximum Q
                        if self.temperature < 0.01:
                            bChoice = bActions[bQ.tolist().index(max(bQ))]
                        else:
                            
                            # Choose action using a probabilistic softmax
                            bPolicy = np.exp(bQ / self.temperature) / np.sum(np.exp(bQ / self.temperature), axis = 0)
                            bChoice = np.random.choice(bActions, p = bPolicy)
                    
                    if wGuaranteedAction != 0:
                        wChoice = wGuaranteedAction
                        wGuaranteedAction = 0
                    else:
                        if np.random.random() < self.epsilon:
                            wQ = np.ones(len(wActions))
                        else:
                            wQ = np.array([])
                            for iAction in range(len(wActions)):
                                wTryTemp = wTryingNow
                                wTryTemp += str(wActions[iAction])
                                if wTryTemp in wStrategyTries:
                                    wQ = np.append(wQ, wStrategyWins[wTryTemp] / wStrategyTries[wTryTemp])
                                else:
                                    wQ = np.append(wQ, self.almostGuaranteed)
                        if self.temperature < 0.01:
                            wChoice = wActions[wQ.tolist().index(max(wQ))]
                        else:
                            wPolicy = np.exp(wQ / self.temperature) / np.sum(np.exp(wQ / self.temperature), axis = 0)
                            wChoice = np.random.choice(wActions, p = wPolicy)
                    
                    # Progress the simulation
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
        
        # Based on the results of the simulations,
        # choose the action resulting in the highest probability of winning
        sim = Game.Game(self.blackTeam, self.whiteTeam, state)
        actions = list(c.actions)
        if sim.trainers[0].pokemon.moves[1].cPP <= 0:
            actions.remove(2)
        Q = np.array([])
        for iAction in range(len(actions)):
            Q = np.append(Q, bStrategyWins[str(actions[iAction])] / bStrategyTries[str(actions[iAction])])
        choice = actions[Q.tolist().index(max(Q))]
        return choice

#