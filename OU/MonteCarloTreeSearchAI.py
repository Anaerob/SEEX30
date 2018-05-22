import numpy as np
import time

import Game
import Constants as c
import RandomAI


class AI:
    
    
    def __init__(self, d, e, l, s, t):
        
        self.almostGuaranteed = 1 + 10 * t
        self.depth = d
        self.epsilon = e
        self.limit = l
        self.search = s
        self.temperature = t
    
    def getAction(self, state):
        
        randomAI = RandomAI.AI()
        strategyTries = [{}, {}]
        strategyWins = [{}, {}]
        for iSearch in range(self.search):
            
            # Initialize a simulation starting from the given state
            sim = Game.Game(False, state)
            for iT in range(2):
                sim.trainers[iT].resetNextAction()
            simStart = sim.round
            simTime = time.time()
            tryingNow = ['', '']
            
            guaranteedAction = 0
            actions = self.getAllowedActions(state)
            for iAction in range(len(actions)):
                if str(actions[iAction]) not in strategyTries[0]:
                    guaranteedAction = actions[iAction]
                    break
            
            while sim.running and sim.round - simStart < self.limit:
                states = [sim.getState(c.amBlack), sim.getState(c.amWhite)]
                
                if sim.round - simStart >= self.depth:
                    if sim.forceSwitch[0] == sim.forceSwitch[1]:
                        sim.trainers[0].setNextAction(randomAI.getAction(states[0]))
                        sim.trainers[1].setNextAction(randomAI.getAction(states[1]))
                    else:
                        for iT in range(2):
                            if sim.forceSwitch[iT]:
                                sim.trainers[iT].setNextAction(randomAI.getAction(states[iT]))
                    sim.progress()
                
                else:
                    if sim.forceSwitch[0] == sim.forceSwitch[1]:
                        choice = []
                        for iT in range(2):
                            if guaranteedAction != 0:
                                choice.append(guaranteedAction)
                                guaranteedAction = 0
                            else:
                                actions = self.getAllowedActions(states[iT])
                                if np.random.random() < self.epsilon:
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
                                    iAction = Q.tolist().index(max(Q))
                                else:
                                    policy = np.exp(Q / self.temperature) / np.sum(np.exp(Q / self.temperature), axis = 0)
                                    iAction = np.random.choice(list(range(len(actions))), p = policy)
                                choice.append(actions[iAction])
                        tryingNow[0] += str(choice[0])
                        tryingNow[1] += str(choice[1])
                        sim.trainers[0].setNextAction(choice[0])
                        sim.trainers[1].setNextAction(choice[1])
                        sim.progress()
                    else:
                        for iT in range(2):
                            if sim.forceSwitch[iT]:
                                actions = self.getAllowedActions(states[iT])
                                if np.random.random() < self.epsilon:
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
                                    iAction = Q.tolist().index(max(Q))
                                else:
                                    policy = np.exp(Q / self.temperature) / np.sum(np.exp(Q / self.temperature), axis = 0)
                                    iAction = np.random.choice(list(range(len(actions))), p = policy)
                                choice = actions[iAction]
                                sim.trainers[iT].setNextAction(choice)
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
        
        # Build final Q from the results of the tree search
        actions = self.getAllowedActions(state)
        Q = np.array([])
        for iAction in range(len(actions)):
            Q = np.append(Q, strategyWins[0][str(actions[iAction])] / strategyTries[0][str(actions[iAction])])
        
        iAction = Q.tolist().index(max(Q))
        choice = actions[iAction]
        return choice
    
    def getAllowedActions(self, state):
        
        sim = Game.Game(False, state)
        if sim.forceSwitch[0]:
            actions = self.getAllowedSwitches(state)
        else:
            actions = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
            for iP in range(1, 7):
                if sim.trainers[0].pokemon[iP].cHP <= 0:
                    actions.remove([iP, 0])
                elif sim.trainers[0].cP == iP:
                    actions.remove([iP, 0])
            for iM in range(1, 5):
                if sim.trainers[0].pokemon[sim.trainers[0].cP].moves[iM].cPP <= 0:
                    actions.remove([0, iM])
            if len(actions) > 1:
                actions.remove([0, 0])
        return actions
    
    def getAllowedSwitches(self, state):
        
        sim = Game.Game(False, state)
        switches = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]
        for iP in range(1, 7):
            if sim.trainers[0].pokemon[iP].cHP <= 0:
                switches.remove([iP, 0])
            elif sim.trainers[0].cP == iP:
                switches.remove([iP, 0])
        return switches

#