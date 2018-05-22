import numpy as np
import time

import Constants as c
import Game
import Load
import MonteCarloTreeSearchAI
import PrintTime

def main():
    
    # Parameters
    nGames = 1000
    depth = 10
    search = 1000
    bEpsilon = 0.2
    bTemperature = 0.2
    wEpsilon = 0.2
    wTemperature = 0.2
    
    # Initialize
    print('Start MCTS benchmark!')
    print('[Total games: %d]' % (2 * nGames))
    print(
        '[Depth: %d, Search: %d, Black epsilon: %1.1f, Black temperature: %1.1f, White epsilon: %1.1f, White temperature: %1.1f]'
        % (depth, search, bEpsilon, bTemperature, wEpsilon, wTemperature))
    HCAI = []
    for i in range(1):
        HCAI.append(c.actions[1])
    for i in range(35):
        HCAI.append(c.actions[0])
    bMCTSAI = MonteCarloTreeSearchAI.AI(c.team2, c.team3, depth, bEpsilon, search, bTemperature)
    bMCTSvHC = 0
    wMCTSAI = MonteCarloTreeSearchAI.AI(c.team3, c.team2, depth, wEpsilon, search, wTemperature)
    wMCTSvHC = 0
    
    # Run the benchmark
    for iGame in range(nGames):
        if iGame % int(nGames / 10) == 0:
            print('Completed ' + str(int(100 * iGame / nGames)) + '%')
        game = Game.Game(c.team2, c.team3)
        while game.running:
            game.trainers[0].setNextAction(bMCTSAI.getAction(game.getState(c.amBlack)))
            game.trainers[1].setNextAction(HCAI[game.round])
            game.progress()
        if game.win[0]:
            bMCTSvHC += 1
        game = Game.Game(c.team2, c.team3)
        while game.running:
            game.trainers[0].setNextAction(HCAI[game.round])
            game.trainers[1].setNextAction(wMCTSAI.getAction(game.getState(c.amWhite)))
            game.progress()
        if game.win[1]:
            wMCTSvHC += 1
    print('Completed 100%')
    
    # Write the results
    resultsFile = open('MCTS_benchmark_results.txt', 'w')
    resultsFile.write('## Monte Carlo Tree Search\n')
    resultsFile.write(
        'Games: ' + str(nGames) + '\n'
        + 'Depth: ' + str(depth) + '\n'
        + 'Search: ' + str(search) + '\n'
        + 'Black epsilon: ' + str(bEpsilon) + '\n'
        + 'Black temperature: ' + str(bTemperature) + '\n'
        + 'White epsilon: ' + str(wEpsilon) + '\n'
        + 'White temperature: ' + str(wTemperature) + '\n\n')
    resultsFile.write('## Black \n\n')
    resultsFile.write('# Win percentage: \n')
    resultsFile.write(str(100 * bMCTSvHC / nGames) + '%\n\n')
    resultsFile.write('## White \n\n')
    resultsFile.write('# Win percentage: \n')
    resultsFile.write(str(100 * wMCTSvHC / nGames) + '%\n\n')
    resultsFile.close()

if __name__ == '__main__':
    startTime = time.time()
    main()
    PrintTime.printTime(time.time() - startTime)

#