import numpy as np
import time

import Game
import Load
import PrintTime
import SoftmaxLinearAI

def main():
    
    # Parameters
    nGames = 1000
    learningRate = 0
    temperature = 0
    
    # Initialize
    bias = Load.loadFloatArray('SL_bias_smooth', 2)
    weights = Load.loadFloatMatrix('SL_weights_smooth', 2, 2)
    SLAI = SoftmaxLinearAI.AI(learningRate, temperature, bias, weights)
    HCAI = []
    HC_string = ''
    game = Game.Game()
    for i in range(game.n - 1):
        HCAI.append(0)
        HC_string += '0'
    for i in range(game.n):
        HCAI.append(1)
        HC_string += '1'
    print('Start SL benchmark!')
    print('[Total games: %d]' % (nGames))
    strategies = {}
    SLvHC = 0
    
    # Run the benchmark
    for iGame in range(nGames):
        if iGame % int(nGames / 10) == 0:
            print('Completed ' + str(int(100 * iGame / nGames)) + '%')
        game = Game.Game()
        SL_string = ''
        while game.running:
            SL_action = SLAI.getAction(game.getFeatures(True))
            SL_string += str(SL_action)
            game.progress([SL_action, HCAI[game.round]])
        if game.win[0]:
            SLvHC += 1
        if SL_string in strategies:
            strategies[SL_string] += 1
        else:
            strategies[SL_string] = 1
    print('Completed 100%')
    
    # Write the results
    resultsFile = open('SL_benchmark_results.txt', 'w')
    resultsFile.write('## Softmax Linear\n')
    resultsFile.write(
        'Games: ' + str(nGames) + '\n'
        + 'Temperature: ' + str(temperature) + '\n\n')
    resultsFile.write('# Optimal strategy usage: \n')
    if HC_string in strategies:
        resultsFile.write(str(100 * strategies[HC_string] / nGames) + '%\n\n')
    else:
        resultsFile.write('Did not use the optimal strategy at all\n\n')
    resultsFile.write('# Win percentage: \n')
    resultsFile.write(str(100 * SLvHC / nGames) + '%\n')
    resultsFile.close()

if __name__ == '__main__':
    startTime = time.time()
    main()
    PrintTime.printTime(time.time() - startTime)

#