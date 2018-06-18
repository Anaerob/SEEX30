import numpy as np
import random

import Sim


class AI:
    
    
    def __init__(self, d, e, l, s, t):
        
        self.almostGuaranteed = 1 + 10 * t
        self.depth = d
        self.epsilon = e
        self.extendSearch = False
        self.limit = l
        self.search = s
        self.searchNotFinished = True
        self.temperature = t
    
    def getAction(self, state):
        
        strategyTries = [{}, {}]
        strategyWins = [{}, {}]
        
        sim = Sim.Sim(state)
        initialActions = self.getAllowedActions(sim.currentHP[0], sim.currentPP[0][sim.currentPokemon[0]], sim.currentPokemon[0], sim.forceSwitch[0])
        
        iSearch = 0
        while self.searchNotFinished or self.extendSearch:
            
            # Initialize a simulation starting from the given state
            sim = Sim.Sim(state)
            for iT in range(2):
                sim.nextAction[iT] = 0
            simStart = sim.round
            tryingNow = ['', '']
            
            guaranteedAction = 0
            for iAction in range(len(initialActions)):
                if str(initialActions[iAction]) not in strategyTries[0]:
                    guaranteedAction = initialActions[iAction]
                    break
            
            while sim.running and sim.round - simStart < self.limit:
                if sim.round - simStart >= self.depth:
                    if sim.forceSwitch[0] == sim.forceSwitch[1]:
                        sim.nextAction[0] = random.choice(self.getAllowedActions(sim.currentHP[0], sim.currentPP[0][sim.currentPokemon[0]], sim.currentPokemon[0], sim.forceSwitch[0]))
                        sim.nextAction[1] = random.choice(self.getAllowedActions(sim.currentHP[1], sim.currentPP[1][sim.currentPokemon[1]], sim.currentPokemon[1], sim.forceSwitch[1]))
                    else:
                        for iT in range(2):
                            if sim.forceSwitch[iT]:
                                sim.nextAction[iT] = random.choice(self.getAllowedActions(sim.currentHP[iT], sim.currentPP[iT][sim.currentPokemon[iT]], sim.currentPokemon[iT], sim.forceSwitch[iT]))
                    sim.progress()
                
                else:
                    if sim.forceSwitch[0] == sim.forceSwitch[1]:
                        nextAction = []
                        for iT in range(2):
                            if guaranteedAction != 0:
                                nextAction.append(guaranteedAction)
                                guaranteedAction = 0
                            else:
                                actions = self.getAllowedActions(sim.currentHP[iT], sim.currentPP[iT][sim.currentPokemon[iT]], sim.currentPokemon[iT], sim.forceSwitch[iT])
                                if random.random() < self.epsilon:
                                    Q = np.ones(len(actions))
                                else:
                                    Q = np.array([])
                                    for iAction in range(len(actions)):
                                        iTry = tryingNow[iT]
                                        iTry += str(actions[iAction])
                                        if iTry in strategyTries[iT]:
                                            Q = np.append(Q, strategyWins[iT][iTry] / strategyTries[iT][iTry])
                                        else:
                                            Q = np.append(Q, self.almostGuaranteed)
                                if self.temperature < 0.01:
                                    iChoice = random.choice([i for i, x in enumerate(Q) if x == max(Q)])
                                else:
                                    policy = np.exp(Q / self.temperature) / np.sum(np.exp(Q / self.temperature), axis = 0)
                                    iChoice = np.random.choice(list(range(len(actions))), p = policy)
                                nextAction.append(actions[iChoice])
                        tryingNow[0] += str(nextAction[0])
                        tryingNow[1] += str(nextAction[1])
                        sim.nextAction[0] = nextAction[0]
                        sim.nextAction[1] = nextAction[1]
                        sim.progress()
                    else:
                        for iT in range(2):
                            if sim.forceSwitch[iT]:
                                if guaranteedAction != 0 and iT == 0:
                                    nextAction = guaranteedAction
                                    guaranteedAction = 0
                                else:
                                    actions = self.getAllowedActions(sim.currentHP[iT], sim.currentPP[iT][sim.currentPokemon[iT]], sim.currentPokemon[iT], sim.forceSwitch[iT])
                                    if random.random() < self.epsilon:
                                        Q = np.ones(len(actions))
                                    else:
                                        Q = np.array([])
                                        for iAction in range(len(actions)):
                                            iTry = tryingNow[iT]
                                            iTry += str(actions[iAction])
                                            if iTry in strategyTries[iT]:
                                                Q = np.append(Q, strategyWins[iT][iTry] / strategyTries[iT][iTry])
                                            else:
                                                Q = np.append(Q, self.almostGuaranteed)
                                    if self.temperature < 0.01:
                                        iChoice = random.choice([i for i, x in enumerate(Q) if x == max(Q)])
                                    else:
                                        policy = np.exp(Q / self.temperature) / np.sum(np.exp(Q / self.temperature), axis = 0)
                                        iChoice = np.random.choice(list(range(len(actions))), p = policy)
                                    nextAction = actions[iChoice]
                                tryingNow[iT] += str(nextAction)
                                sim.nextAction[iT] = nextAction
                                sim.progress()
            
            # Update and extend the search tree
            for iT in range(2):
                for subStrategy in range(1, min(sim.round - simStart, self.depth) + 1):
                    if tryingNow[iT][0:6 * subStrategy] in strategyTries[iT]:
                        strategyTries[iT][tryingNow[iT][0:6 * subStrategy]] += 1
                        if sim.win[0]:
                            strategyWins[iT][tryingNow[iT][0:6 * subStrategy]] += 1
                    else:
                        strategyTries[iT][tryingNow[iT][0:6 * subStrategy]] = 1
                        if sim.win[0]:
                            strategyWins[iT][tryingNow[iT][0:6 * subStrategy]] = 1
                        else:
                            strategyWins[iT][tryingNow[iT][0:6 * subStrategy]] = 0
                        break
            
            iSearch += 1
            self.searchNotFinished = iSearch < self.search
        self.searchNotFinished = True
        
        # Build final Q from the results of the tree search
        Q = np.array([])
        for iAction in range(len(initialActions)):
            Q = np.append(Q, strategyWins[0][str(initialActions[iAction])] / strategyTries[0][str(initialActions[iAction])])
        
        return initialActions[random.choice([i for i, x in enumerate(Q) if x == max(Q)])]
    
    def getAllowedActions(self, chp, cpp, cp, fs):
        
        if fs:
            actions = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]
            for iP in range(1, 7):
                if chp[iP] <= 0:
                    actions.remove([iP, 0])
                elif cp == iP:
                    actions.remove([iP, 0])
        else:
            actions = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
            for iP in range(1, 7):
                if chp[iP] <= 0:
                    actions.remove([iP, 0])
                elif cp == iP:
                    actions.remove([iP, 0])
            for iM in range(1, 5):
                if cpp[iM] <= 0:
                    actions.remove([0, iM])
            if len(actions) == 0:
                actions = [[0, 0]]
        return actions

#