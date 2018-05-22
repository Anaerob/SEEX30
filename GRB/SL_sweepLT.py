import numpy as np
import time

import Constants as c
import Game
import Load
import PrintTime
import SoftmaxLinearAI

def main():
    
    # Parameters
    nBenchmark = 1000
    nTrain = 20000
    nCut = int(nTrain / 2)
    nRepeat = 100
    decay = 1
    learningRate = [0.1, 0.2, 0.3, 0.4, 0.5]
    temperature = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    # Initialize the parameter sweep
    infoFile = open('SL_sweepLT_info.txt', 'w')
    infoFile.write(
        'Benchmark = ' + str(nBenchmark) + '\n'
        + 'Cut = ' + str(nCut) + '\n'
        + 'Train = ' + str(nTrain) + '\n'
        + 'Repeat = ' + str(nRepeat) + '\n'
        + 'Decay = ' + str(decay) + '\n'
        + 'Learning rate = ' + str(learningRate) + '\n'
        + 'Temperature = ' + str(temperature) + '\n')
    infoFile.close()
    print('Start SL learning rate and temperature sweep!')
    print('[Total games: %d]' % (nRepeat * (nTrain + 2 * nBenchmark) * len(learningRate) * len(temperature)))
    print(
        '[Decay: %1.1f]'
        % (decay))
    
    bAvgResultsFile = open('SL_sweepLT_bAvg.txt', 'w')
    bMaxResultsFile = open('SL_sweepLT_bMax.txt', 'w')
    wAvgResultsFile = open('SL_sweepLT_wAvg.txt', 'w')
    wMaxResultsFile = open('SL_sweepLT_wMax.txt', 'w')
    
    # Run the parameter sweep
    for iLearningRate in range(len(learningRate)):
        for iTemperature in range(len(temperature)):
            print(
                'Completed %1.1f'
                % (100 * (iLearningRate * len(temperature) + iTemperature)
                    / (len(learningRate) * len(temperature)))
                + '%')
            bMaxSLvHC = 0
            bSumSLvHC = 0
            wMaxSLvHC = 0
            wSumSLvHC = 0
            for iRepeat in range(nRepeat):
                
                # Initialize the training
                bAI = SoftmaxLinearAI.AI(learningRate[iLearningRate], temperature[iTemperature])
                bBiasAll = []
                bWeightsAll = []
                wAI = SoftmaxLinearAI.AI(learningRate[iLearningRate], temperature[iTemperature])
                wBiasAll = []
                wWeightsAll = []
                
                # Run the training
                for iTrain in range(nTrain):
                    game = Game.Game(c.team2, c.team3)
                    bActions = []
                    bFeatures = []
                    wActions = []
                    wFeatures = []
                    while game.running:
                        bFeatures.append(game.getFeatures(c.amBlack))
                        bActions.append(bAI.getAction(bFeatures[game.round]))
                        game.trainers[0].setNextAction(bActions[game.round])
                        wFeatures.append(game.getFeatures(c.amWhite))
                        wActions.append(wAI.getAction(wFeatures[game.round]))
                        game.trainers[1].setNextAction(wActions[game.round])
                        game.progress()
                    
                    # Train the AI based on the results
                    # Reward 1 for winning and -1 for losing
                    if game.win[0]:
                        for iRound in range(game.round):
                            bAI.train(bFeatures[game.round - iRound - 1], bActions[game.round - iRound - 1], 1 * (decay ** iRound))
                            wAI.train(wFeatures[game.round - iRound - 1], wActions[game.round - iRound - 1], -1 * (decay ** iRound))
                    if game.win[1]:
                        for iRound in range(game.round):
                            bAI.train(bFeatures[game.round - iRound - 1], bActions[game.round - iRound - 1], -1 * (decay ** iRound))
                            wAI.train(wFeatures[game.round - iRound - 1], wActions[game.round - iRound - 1], 1 * (decay ** iRound))
                    
                    if iTrain >= nCut:
                        bBiasAll.append(bAI.bias.tolist())
                        bWeightsAll.append(bAI.weights.tolist())
                        wBiasAll.append(wAI.bias.tolist())
                        wWeightsAll.append(wAI.weights.tolist())
                bBiasSmooth = np.sum(bBiasAll, axis=0) / (nTrain - nCut)
                bWeightsSmooth = np.sum(bWeightsAll, axis=0) / (nTrain - nCut)
                wBiasSmooth = np.sum(wBiasAll, axis=0) / (nTrain - nCut)
                wWeightsSmooth = np.sum(wWeightsAll, axis=0) / (nTrain - nCut)
                
                # Initialize the benchmark
                bAI = SoftmaxLinearAI.AI(0, 0, bBiasSmooth, bWeightsSmooth)
                wAI = SoftmaxLinearAI.AI(0, 0, wBiasSmooth, wWeightsSmooth)
                HCAI = []
                for i in range(1):
                    HCAI.append(2)
                for i in range(35):
                    HCAI.append(1)
                bSLvHC = 0
                wSLvHC = 0
                
                # Run the benchmark
                for iBenchmark in range(nBenchmark):
                    game = Game.Game(c.team2, c.team3)
                    while game.running:
                        game.trainers[0].setNextAction(bAI.getAction(game.getFeatures(c.amBlack)))
                        game.trainers[1].setNextAction(HCAI[game.round])
                        game.progress()
                    if game.win[0]:
                        bSLvHC += 1
                    game = Game.Game(c.team2, c.team3)
                    while game.running:
                        game.trainers[0].setNextAction(HCAI[game.round])
                        game.trainers[1].setNextAction(wAI.getAction(game.getFeatures(c.amWhite)))
                        game.progress()
                    if game.win[1]:
                        wSLvHC += 1
                if bSLvHC / nBenchmark > bMaxSLvHC:
                    bMaxSLvHC = bSLvHC / nBenchmark
                if wSLvHC / nBenchmark > wMaxSLvHC:
                    wMaxSLvHC = wSLvHC / nBenchmark
                bSumSLvHC += bSLvHC / nBenchmark
                wSumSLvHC += wSLvHC / nBenchmark
            bAvgResultsFile.write(str(bSumSLvHC / nRepeat) + '\n')
            bMaxResultsFile.write(str(bMaxSLvHC) + '\n')
            wAvgResultsFile.write(str(wSumSLvHC / nRepeat) + '\n')
            wMaxResultsFile.write(str(wMaxSLvHC) + '\n')
    bAvgResultsFile.close()
    bMaxResultsFile.close()
    wAvgResultsFile.close()
    wMaxResultsFile.close()
    print('Completed 100%')

if __name__ == '__main__':
    startTime = time.time()
    main()
    PrintTime.printTime(time.time() - startTime)

#