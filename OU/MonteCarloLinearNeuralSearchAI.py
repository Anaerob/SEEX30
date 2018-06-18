import random
import time

import Sim
import LinearNeuralNetworkAI

class AI:
    
    
    def __init__(self, l, m, s):
        
        self.extendSearch = False
        self.iSearch = 0
        self.limit = l
        self.minimum = m
        self.search = s
        self.searchAI = LinearNeuralNetworkAI.AI(0, 0, True)
        self.searchNotFinished = True
    
    def getAction(self, state):
        
        if state[6][0] and not state[4][0]:
            return [0, 0]
        else:
            
            # Get all allowed initial actions
            initialActions = self.getAllowedActions(state[14][0], state[15][0][state[3][0] - 1], state[3][0], state[4][0])
            nInitialActions = len(initialActions)
            
            if nInitialActions == 1:
                return initialActions[0]
            else:
                strategyTries = []
                strategyWins = []
                
                startTime = time.time()
                for iObligatory in range(nInitialActions):
                    
                    # Initialize a simulation starting from the given state
                    sim = Sim.Sim(state)
                    sim.nextAction[0] = 0
                    sim.nextAction[1] = 0
                    simStart = sim.round
                    
                    # Do obligatory initial action
                    if sim.forceSwitch[0] == sim.forceSwitch[1]:
                        sim.nextAction[0] = initialActions[iObligatory]
                        sim.nextAction[1] = self.searchAI.getAction(sim.getState(False))
                    elif sim.forceSwitch[0]:
                        sim.nextAction[0] = initialActions[iObligatory]
                    sim.progress()
                    
                    # Play out game randomly
                    while sim.running and sim.round < self.limit:
                        if sim.forceSwitch[0] == sim.forceSwitch[1]:
                            sim.nextAction[0] = self.searchAI.getAction(sim.getState(True))
                            sim.nextAction[1] = self.searchAI.getAction(sim.getState(False))
                        elif sim.forceSwitch[0]:
                            sim.nextAction[0] = self.searchAI.getAction(sim.getState(True))
                        elif sim.forceSwitch[1]:
                            sim.nextAction[1] = self.searchAI.getAction(sim.getState(False))
                        sim.progress()
                    
                    # Initialize search results
                    strategyTries.append(1)
                    strategyWins.append(int(sim.win[0]))
                
                self.iSearch = 0
                self.searchNotFinished = time.time() - startTime < self.search
                while self.iSearch < self.minimum or self.searchNotFinished or self.extendSearch:
                    
                    # Initialize a simulation starting from the given state
                    sim = Sim.Sim(state)
                    sim.nextAction[0] = 0
                    sim.nextAction[1] = 0
                    simStart = sim.round
                    
                    # Rotate initial actions for even sampling
                    if sim.forceSwitch[0] == sim.forceSwitch[1]:
                        sim.nextAction[0] = initialActions[self.iSearch % nInitialActions]
                        sim.nextAction[1] = self.searchAI.getAction(sim.getState(False))
                    elif sim.forceSwitch[0]:
                        sim.nextAction[0] = initialActions[self.iSearch % nInitialActions]
                    sim.progress()
                    
                    # Play out game randomly
                    while sim.running and sim.round < self.limit:
                        if sim.forceSwitch[0] == sim.forceSwitch[1]:
                            sim.nextAction[0] = self.searchAI.getAction(sim.getState(True))
                            sim.nextAction[1] = self.searchAI.getAction(sim.getState(False))
                        elif sim.forceSwitch[0]:
                            sim.nextAction[0] = self.searchAI.getAction(sim.getState(True))
                        elif sim.forceSwitch[1]:
                            sim.nextAction[1] = self.searchAI.getAction(sim.getState(False))
                        sim.progress()
                    
                    # Update search
                    strategyTries[self.iSearch % nInitialActions] += 1
                    strategyWins[self.iSearch % nInitialActions] += int(sim.win[0])
                    self.iSearch += 1
                    self.searchNotFinished = time.time() - startTime < self.search
                
                # Build final Q from the results of the search
                Q = []
                for iAction in range(nInitialActions):
                    Q.append(strategyWins[iAction] / strategyTries[iAction])
                
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