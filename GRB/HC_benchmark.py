import numpy as np
import time

import Constants as c
import Game
import Load
import PrintTime

def main():
    
    # Parameters
    nGames = 1000000
    bWeakening = 1
    wWeakening = 1
    
    # Initialize
    print('Start benchmark!')
    print('[Total games: %d]' % ((nGames)))
    resultsFile = open('HC_benchmark_results.txt', 'w')
    resultsFile.write('### Hard Coded\n')
    resultsFile.write('Games: ' + str(nGames) + '\n\n')
    bHCAI = []
    wHCAI = []
    for i in range(bWeakening):
        bHCAI.append(c.actions[1])
    for i in range(wWeakening):
        wHCAI.append(c.actions[1])
    for i in range(35):
        bHCAI.append(c.actions[0])
        wHCAI.append(c.actions[0])
    bWin = 0
    
    # Run the benchmark
    for iGame in range(nGames):
        game = Game.Game(c.team2, c.team3)
        while game.running:
            game.trainers[0].setNextAction(bHCAI[game.round])
            game.trainers[1].setNextAction(wHCAI[game.round])
            game.progress()
        if game.win[0]:
            bWin += 1
    
    # Write the results
    resultsFile.write('## Black \n\n')
    resultsFile.write('# Win percentage: \n')
    resultsFile.write(str(100 * bWin / nGames) + '%\n\n')
    resultsFile.write('## White \n\n')
    resultsFile.write('# Win percentage: \n')
    resultsFile.write(str(100 * (nGames - bWin) / nGames) + '%\n\n')
    resultsFile.close()

if __name__ == '__main__':
    startTime = time.time()
    main()
    PrintTime.printTime(time.time() - startTime)

#