import numpy as np
import time

import Constants as c
import Game
import Load
import PrintTime
import SoftmaxLinearAI

def main():
    
    # Parameters
    nTrain = 20000
    nPlotPoints = 1000
    nCut = int(nPlotPoints / 2)
    decay = 1
    bLearningRate = 0.1
    bTemperature = 0.1
    wLearningRate = 0.1
    wTemperature = 0.2
    
    # Initialize
    infoFile = open('SL_train_info.txt', 'w')
    infoFile.write(
        'Games = ' + str(nTrain) + '\n'
        + 'Decay = ' + str(decay) + '\n'
        + 'Black learning rate = ' + str(bLearningRate) + '\n'
        + 'Black temperature = ' + str(bTemperature) + '\n'
        + 'White learning rate = ' + str(wLearningRate) + '\n'
        + 'White temperature = ' + str(wTemperature) + '\n')
    infoFile.close()
    print('Start SL training!')
    print('[Total games: %d]' % (nTrain))
    print(
        '[Decay: %1.1f, Black learning rate: %1.2f, Black temperature: %1.2f, White learning rate: %1.2f, White temperature: %1.2f]'
        % (decay, bLearningRate, bTemperature, wLearningRate, wTemperature))
    bAI = SoftmaxLinearAI.AI(bLearningRate, bTemperature)
    bBiasPlotFile = open('SL_bBias_plot.txt', 'w')
    bWeightsPlotFile = open('SL_bWeights_plot.txt', 'w')
    wAI = SoftmaxLinearAI.AI(wLearningRate, wTemperature)
    wBiasPlotFile = open('SL_wBias_plot.txt', 'w')
    wWeightsPlotFile = open('SL_wWeights_plot.txt', 'w')
    
    # Run the training
    for iTrain in range(nTrain):
        if iTrain % int(nTrain / 10) == 0:
            print('Completed ' + str(int(100 * iTrain / nTrain)) + '%')
        
        # Save weights for the plot
        if iTrain % int(nTrain / nPlotPoints) == 0:
            for i in range(c.nOutputs):
                bBiasPlotFile.write(str(bAI.bias[i]) + '\n')
                wBiasPlotFile.write(str(wAI.bias[i]) + '\n')
                for j in range(c.nInputs):
                    bWeightsPlotFile.write(str(bAI.weights[i][j]) + '\n')
                    wWeightsPlotFile.write(str(wAI.weights[i][j]) + '\n')
        
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
    
    print('Completed 100%')
    
    # Save final biases and weights
    bBiasFinalFile = open('SL_bBias_final.txt', 'w')
    bWeightsFinalFile = open('SL_bWeights_final.txt', 'w')
    wBiasFinalFile = open('SL_wBias_final.txt', 'w')
    wWeightsFinalFile = open('SL_wWeights_final.txt', 'w')
    for i in range(c.nOutputs):
        bBiasFinalFile.write(str(bAI.bias[i]) + '\n')
        bBiasPlotFile.write(str(bAI.bias[i]) + '\n')
        wBiasFinalFile.write(str(wAI.bias[i]) + '\n')
        wBiasPlotFile.write(str(wAI.bias[i]) + '\n')
        for j in range(c.nInputs):
            bWeightsFinalFile.write(str(bAI.weights[i][j]) + '\n')
            bWeightsPlotFile.write(str(bAI.weights[i][j]) + '\n')
            wWeightsFinalFile.write(str(wAI.weights[i][j]) + '\n')
            wWeightsPlotFile.write(str(wAI.weights[i][j]) + '\n')
    bBiasFinalFile.close()
    bBiasPlotFile.close()
    bWeightsFinalFile.close()
    bWeightsPlotFile.close()
    wBiasFinalFile.close()
    wBiasPlotFile.close()
    wWeightsFinalFile.close()
    wWeightsPlotFile.close()
    
    # Smooth the biases and weights
    bBiasPlot = Load.loadFloatMatrix('SL_bBias_plot', nPlotPoints + 1, c.nOutputs)
    bWeightsPlot = Load.loadFloatMatrix('SL_bWeights_plot', nPlotPoints + 1, c.nOutputs * c.nInputs)
    wBiasPlot = Load.loadFloatMatrix('SL_wBias_plot', nPlotPoints + 1, c.nOutputs)
    wWeightsPlot = Load.loadFloatMatrix('SL_wWeights_plot', nPlotPoints + 1, c.nOutputs * c.nInputs)
    bBiasSmooth = np.sum(bBiasPlot[nCut:(nPlotPoints + 1)], axis = 0) / (nPlotPoints + 1 - nCut)
    bWeightsSmooth = np.sum(bWeightsPlot[nCut:(nPlotPoints + 1)], axis = 0) / (nPlotPoints + 1 - nCut)
    wBiasSmooth = np.sum(wBiasPlot[nCut:(nPlotPoints + 1)], axis = 0) / (nPlotPoints + 1 - nCut)
    wWeightsSmooth = np.sum(wWeightsPlot[nCut:(nPlotPoints + 1)], axis = 0) / (nPlotPoints + 1 - nCut)
    bBiasSmoothFile = open('SL_bBias_smooth.txt', 'w')
    bWeightsSmoothFile = open('SL_bWeights_smooth.txt', 'w')
    wBiasSmoothFile = open('SL_wBias_smooth.txt', 'w')
    wWeightsSmoothFile = open('SL_wWeights_smooth.txt', 'w')
    for i in range(c.nOutputs):
        bBiasSmoothFile.write(str(bBiasSmooth[i]) + '\n')
        wBiasSmoothFile.write(str(wBiasSmooth[i]) + '\n')
    for i in range(c.nOutputs * c.nInputs):
        bWeightsSmoothFile.write(str(bWeightsSmooth[i]) + '\n')
        wWeightsSmoothFile.write(str(wWeightsSmooth[i]) + '\n')
    bBiasSmoothFile.close()
    bWeightsSmoothFile.close()
    wBiasSmoothFile.close()
    wWeightsSmoothFile.close()

if __name__ == '__main__':
    startTime = time.time()
    main()
    PrintTime.printTime(time.time() - startTime)

#