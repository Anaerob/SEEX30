import numpy as np
import os
import time

import FormatTime
import Game
import LinearNeuralNetworkAI
import RandomAI
import Sim

def benchmarkAI(AI, nBench, parameters):
    
    AI.learningRate = 0
    AI.temperature = 0
    RAI = RandomAI.AI()
    iWin = 0
    
    for iBench in range(nBench):
        game = Game.Game()
        while game.running and game.round < parameters[7]:
            if game.forceSwitch[0] == game.forceSwitch[1]:
                game.nextAction[0] = AI.getAction(game.getState(True))
                game.nextAction[1] = RAI.getAction(game.getState(False))
            elif game.forceSwitch[0]:
                game.nextAction[0] = AI.getAction(game.getState(True))
            elif game.forceSwitch[1]:
                game.nextAction[1] = RAI.getAction(game.getState(False))
            game.progress()
        if game.win[0]:
            iWin += 1
    
    return iWin

def trainAI(AI, nAverage, nTrain, parameters):
    
    AI.learningRate = parameters[4]
    AI.temperature = parameters[5]
    
    averageMoveBias = np.zeros((6, 6, 4))
    averageMoveWeights = np.zeros((6, 6, 4, 15))
    averageSwitchBias = np.zeros((6, 6))
    averageSwitchWeights = np.zeros((6, 6, 14))
    
    for iTrain in range(nTrain):
        sim = Sim.Sim()
        actions = [[], []]
        states = [[], []]
        nActions = [0, 0]
        while sim.running and sim.round < parameters[7]:
            if sim.forceSwitch[0] == sim.forceSwitch[1]:
                
                states[0].append(sim.getState(True))
                actions[0].append(AI.getAction(states[0][nActions[0]]))
                sim.nextAction[0] = actions[0][nActions[0]]
                nActions[0] += 1
                
                states[1].append(sim.getState(False))
                actions[1].append(AI.getAction(states[1][nActions[1]]))
                sim.nextAction[1] = actions[1][nActions[1]]
                nActions[1] += 1
                
            elif sim.forceSwitch[0]:
                
                states[0].append(sim.getState(True))
                actions[0].append(AI.getAction(states[0][nActions[0]]))
                sim.nextAction[0] = actions[0][nActions[0]]
                nActions[0] += 1
                
            elif sim.forceSwitch[1]:
                
                states[1].append(sim.getState(False))
                actions[1].append(AI.getAction(states[1][nActions[1]]))
                sim.nextAction[1] = actions[1][nActions[1]]
                nActions[1] += 1
                
            sim.progress()
        
        # Train the AI based on the results
        # Reward 1 for winning and -1 for losing
        if sim.win[0]:
            for iAction in range(nActions[0]):
                AI.train(actions[0][iAction], 1, states[0][iAction])
        else:
            for iAction in range(nActions[0]):
                AI.train(actions[0][iAction], -1, states[0][iAction])
        if sim.win[1]:
            for iAction in range(nActions[1]):
                AI.train(actions[1][iAction], 1, states[1][iAction])
        else:
            for iAction in range(nActions[1]):
                AI.train(actions[1][iAction], -1, states[1][iAction])
        
        if (iTrain + 1) % (nTrain / nAverage) == 0:
            for iO in range(6):
                for iP in range(6):
                    averageSwitchBias[iO][iP] += AI.switchBias[iO][iP] / nAverage
                    for iM in range(4):
                        averageMoveBias[iO][iP][iM] += AI.moveBias[iO][iP][iM] / nAverage
                        for iF in range(15):
                            averageMoveWeights[iO][iP][iM][iF] += AI.moveWeights[iO][iP][iM][iF] / nAverage
                    for iF in range(14):
                        averageSwitchWeights[iO][iP][iF] += AI.switchWeights[iO][iP][iF] / nAverage
    
    for iO in range(6):
        for iP in range(6):
            AI.switchBias[iO][iP] = averageSwitchBias[iO][iP]
            for iM in range(4):
                AI.moveBias[iO][iP][iM] = averageMoveBias[iO][iP][iM]
                for iF in range(15):
                    AI.moveWeights[iO][iP][iM][iF] = averageMoveWeights[iO][iP][iM][iF]
            for iF in range(14):
                AI.switchWeights[iO][iP][iF] = averageSwitchWeights[iO][iP][iF]

def printInterface(bAverage, bBench, bInitial, currentWin, globalMaxWin, localMaxWin, parameters, round):
    
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    
    print()
    
    if bAverage:
        print('Currently training AI!')
        print()
    elif bBench:
        print('Currently benchmarking AI!')
        print()
    elif bInitial:
        print('Currently initializing AI!')
        print()
    
    if globalMaxWin != 0:
        print('Global max: ' + str(100 * globalMaxWin / parameters[1]) + '% win ')
        print()
    
    if round != 0:
        print('Round: ' + str(round))
        if localMaxWin != 0:
            print('Local max: ' + str(100 * localMaxWin / parameters[1]) + '% win ')
        if currentWin != 0:
            print('Current: ' + str(100 * currentWin / parameters[1]) + '% win ')

def main():
    
    # Parameters
    nAverage = 10
    nBench = 100
    nInitial = 10000
    nTrain = 1000
    learningRate = 0.01
    temperature = 0.1
    tolerance = 0.75
    limit = 100
    parameters = [nAverage, nBench, nInitial, nTrain, learningRate, temperature, tolerance, limit]
    
    printInterface(False, True, False, 0, 0, 0, parameters, 0)
    
    # Initialize
    if not os.path.isfile('LinearNeuralNetworkAI/moveBias.txt'):
        LNNAI = LinearNeuralNetworkAI.AI(learningRate, temperature, False)
        LNNAI.save()
        globalMaxWin = benchmarkAI(LNNAI, nBench, parameters)
        printInterface(False, False, True, 0, globalMaxWin, 0, parameters, 0)
    else:
        LNNAI = LinearNeuralNetworkAI.AI(learningRate, temperature, True)
        globalMaxWin = benchmarkAI(LNNAI, nBench, parameters)
        printInterface(False, False, True, 0, globalMaxWin, 0, parameters, 1)
    
    # Start training process
    round = 0
    while globalMaxWin != nBench:
        round += 1
        
        LNNAI = LinearNeuralNetworkAI.AI(learningRate, temperature, False)
        trainAI(LNNAI, 1, nInitial, parameters)
        trained = nInitial
        printInterface(False, True, False, 0, globalMaxWin, 0, parameters, round)
        
        currentWin = benchmarkAI(LNNAI, nBench, parameters)
        localMaxWin = currentWin
        printInterface(True, False, False, currentWin, globalMaxWin, localMaxWin, parameters, round)
        
        while currentWin >= localMaxWin * tolerance:
            
            trainAI(LNNAI, nAverage, nTrain, parameters)
            trained += nTrain
            printInterface(False, True, False, currentWin, globalMaxWin, localMaxWin, parameters, round)
            
            currentWin = benchmarkAI(LNNAI, nBench, parameters)
            printInterface(True, False, False, currentWin, globalMaxWin, localMaxWin, parameters, round)
            
            if currentWin > localMaxWin:
                localMaxWin = currentWin
                printInterface(True, False, False, currentWin, globalMaxWin, localMaxWin, parameters, round)
                if localMaxWin > globalMaxWin:
                    globalMaxWin = localMaxWin
                    printInterface(True, False, False, currentWin, globalMaxWin, localMaxWin, parameters, round)
                    LNNAI.save()
        printInterface(False, False, True, currentWin, globalMaxWin, localMaxWin, parameters, round + 1)

if __name__ == '__main__':
    main()

#