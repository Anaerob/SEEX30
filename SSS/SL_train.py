import numpy as np
import time

import Game
import Load
import PrintTime
import SoftmaxLinearAI

def main():
    
    # Parameters
    nTrain = 1000000
    decay = 1
    learningRate = 0.05
    temperature = 0.2
    nPlotPoints = 1000
    
    # Initialize
    startTime = time.time()
    AI = SoftmaxLinearAI.AI(learningRate, temperature)
    infoFile = open('SL_train_info.txt', 'w')
    infoFile.write(
        'Games = ' + str(nTrain) + '\n'
        + 'Decay = ' + str(decay) + '\n'
        + 'Learning rate = ' + str(learningRate) + '\n'
        + 'Temperature = ' + str(temperature) + '\n')
    infoFile.close()
    print('Start SL training!')
    print('[Total games: %d]' % (nTrain))
    print(
        '[Decay: %1.1f, Learning rate: %1.2f, Temperature: %1.1f]'
        % (decay, learningRate, temperature))
    biasPlotFile = open('SL_bias_plot.txt', 'w')
    weightsPlotFile = open('SL_weights_plot.txt', 'w')
    
    # Run the training
    for iTrain in range(nTrain):
        if iTrain % int(nTrain / 10) == 0:
            print('Completed ' + str(int(100 * iTrain / nTrain)) + '%')
        
        # Save biases and weights for the plot
        if iTrain % int(nTrain / nPlotPoints) == 0:
            for i in range(2):
                biasPlotFile.write(str(AI.bias[i]) + '\n')
                for j in range(2):
                    weightsPlotFile.write(str(AI.weights[i][j]) + '\n')
        
        game = Game.Game()
        bFeatures = []
        bActions = []
        wFeatures = []
        wActions = []
        while game.running:
            bFeatures.append(game.getFeatures(True))
            bActions.append(AI.getAction(bFeatures[game.round]))
            wFeatures.append(game.getFeatures(False))
            wActions.append(AI.getAction(wFeatures[game.round]))
            game.progress([bActions[game.round], wActions[game.round]])
        
        # Train the AI based on the results
        # Reward 1 for winning and -1 for losing
        if game.win[0]:
            for iRound in range(game.round):
                AI.train(
                    bFeatures[game.round - iRound - 1],
                    bActions[game.round - iRound - 1],
                    1 * (decay ** iRound))
                AI.train(
                    wFeatures[game.round - iRound - 1],
                    wActions[game.round - iRound - 1],
                    -1 * (decay ** iRound))
        if game.win[1]:
            for iRound in range(game.round):
                AI.train(
                    bFeatures[game.round - iRound - 1],
                    bActions[game.round - iRound - 1],
                    -1 * (decay ** iRound))
                AI.train(
                    wFeatures[game.round - iRound - 1],
                    wActions[game.round - iRound - 1],
                    1 * (decay ** iRound))
        
    print('Completed 100%')
    
    # Save final biases and weights
    biasFinalFile = open('SL_bias_final.txt', 'w')
    weightsFinalFile = open('SL_weights_final.txt', 'w')
    for i in range(2):
        biasFinalFile.write(str(AI.bias[i]) + '\n')
        biasPlotFile.write(str(AI.bias[i]) + '\n')
        for j in range(2):
            weightsFinalFile.write(str(AI.weights[i][j]) + '\n')
            weightsPlotFile.write(str(AI.weights[i][j]) + '\n')
    biasFinalFile.close()
    biasPlotFile.close()
    weightsFinalFile.close()
    weightsPlotFile.close()
    
    # Smooth the biases and weights
    biasPlot = Load.loadFloatMatrix('SL_bias_plot', nPlotPoints + 1, 2)
    weightsPlot = Load.loadFloatMatrix('SL_weights_plot', nPlotPoints + 1, 2 * 2)
    biasSmooth = np.sum(biasPlot, axis = 0) / (nPlotPoints + 1)
    weightsSmooth = np.sum(weightsPlot, axis = 0) / (nPlotPoints + 1)
    biasSmoothFile = open('SL_bias_smooth.txt', 'w')
    weightsSmoothFile = open('SL_weights_smooth.txt', 'w')
    for i in range(2):
        biasSmoothFile.write(str(biasSmooth[i]) + '\n')
    for i in range(4):
        weightsSmoothFile.write(str(weightsSmooth[i]) + '\n')
    biasSmoothFile.close()
    weightsSmoothFile.close()
    
    PrintTime.printTime(time.time() - startTime)
    
if __name__ == '__main__':
    main()

#