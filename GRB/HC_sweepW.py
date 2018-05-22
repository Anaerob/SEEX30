import numpy as np
import time

import Constants as c
import Game
import Load
import PrintTime

def main():
    
    # Parameters
    nGames = 1000000
    nStrategies = 7
    
    # Initialize
    infoFile = open('HC_sweepW_info.txt', 'w')
    infoFile.write(
        'Games = ' + str(nGames) + '\n'
        + 'Strategies = ' + str(nStrategies) + '\n')
    infoFile.close()
    print('Start HC weakening sweep!')
    print('[Total games: %d]' % (nGames * nStrategies ** 2))
    strategy = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    strategies = [strategy.copy()]
    for i in range(nStrategies - 1):
        strategy.insert(0, 2)
        strategies.append(strategy.copy())
    resultsFile = open('HC_sweepW.txt', 'w')
    
    # Run the sweep
    for iStrategy in range(nStrategies):
        for jStrategy in range(nStrategies):
            print('Completed %1.1f' % (100 * (iStrategy * nStrategies + jStrategy) / (nStrategies ** 2)) + '%')
            bWin = 0
            for iGame in range(nGames):
                game = Game.Game(c.team2, c.team3)
                while game.running:
                    game.trainers[0].setNextAction(strategies[iStrategy][game.round])
                    game.trainers[1].setNextAction(strategies[jStrategy][game.round])
                    game.progress()
                if game.win[0]:
                    bWin += 1
            resultsFile.write(str(bWin / nGames) + '\n')
    resultsFile.close()
    
    # Calculate optimal number of weakening moves
    sweepResults = Load.loadFloatMatrix('HC_sweepW', nStrategies, nStrategies)
    optimalFile = open('HC_optimal.txt', 'w')
    optimalFile.write('### Hard Coded\n')
    optimalFile.write('## Optimal number of weakening moves\n\n')
    bOptimal = np.sum(sweepResults, axis = 0) / nStrategies
    optimalFile.write('# Charmander: ' + str(bOptimal.tolist().index(min(bOptimal))) + '\n\n')
    wOptimal = np.sum(sweepResults, axis = 1) / nStrategies
    optimalFile.write('# Squirtle: ' + str(wOptimal.tolist().index(max(wOptimal))) + '\n\n')

if __name__ == '__main__':
    startTime = time.time()
    main()
    PrintTime.printTime(time.time() - startTime)

#