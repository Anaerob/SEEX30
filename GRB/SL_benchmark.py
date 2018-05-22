import numpy as np
import time

import Constants as c
import Game
import Load
import PrintTime
import SoftmaxLinearAI

def main():
    
    # Parameters
    nGames = 1000000
    learningRate = 0
    temperature = 0
    
    # Initialize
    print('Start benchmark!')
    print('[Total games: %d]' % ((2 * nGames)))
    bBias = Load.loadFloatArray('SL_bBias_smooth', c.nOutputs)
    bWeights = Load.loadFloatMatrix('SL_bWeights_smooth', c.nOutputs, c.nInputs)
    bSLAI = SoftmaxLinearAI.AI(learningRate, temperature, bBias, bWeights)
    wBias = Load.loadFloatArray('SL_wBias_smooth', c.nOutputs)
    wWeights = Load.loadFloatMatrix('SL_wWeights_smooth', c.nOutputs, c.nInputs)
    wSLAI = SoftmaxLinearAI.AI(learningRate, temperature, wBias, wWeights)
    HCAI = []
    for i in range(1):
        HCAI.append(2)
    for i in range(35):
        HCAI.append(1)
    bSLvHC = 0
    wSLvHC = 0
    
    # Run the benchmark
    for iGame in range(nGames):
        game = Game.Game(c.team2, c.team3)
        while game.running:
            game.trainers[0].setNextAction(bSLAI.getAction(game.getFeatures(c.amBlack)))
            game.trainers[1].setNextAction(HCAI[game.round])
            game.progress()
        if game.win[0]:
            bSLvHC += 1
        game = Game.Game(c.team2, c.team3)
        while game.running:
            game.trainers[0].setNextAction(HCAI[game.round])
            game.trainers[1].setNextAction(wSLAI.getAction(game.getFeatures(c.amWhite)))
            game.progress()
        if game.win[1]:
            wSLvHC += 1
    
    # Write the results
    resultsFile = open('SL_benchmark_results.txt', 'w')
    resultsFile.write('### Softmax Linear\n')
    resultsFile.write('Games: ' + str(nGames) + '\n\n')
    resultsFile.write('## Black \n\n')
    resultsFile.write('# Win percentage: \n')
    resultsFile.write(str(100 * bSLvHC / nGames) + '%\n\n')
    resultsFile.write('## White \n\n')
    resultsFile.write('# Win percentage: \n')
    resultsFile.write(str(100 * wSLvHC / nGames) + '%\n\n')
    resultsFile.close()

if __name__ == '__main__':
    startTime = time.time()
    main()
    PrintTime.printTime(time.time() - startTime)

#