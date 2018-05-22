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
    depth = 5
    epsilon = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    search = 200
    temperature = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    
    # Initialize
    infoFile = open('MCTS_sweepET_info.txt', 'w')
    infoFile.write(
        'Games = ' + str(nGames) + '\n'
        + 'Depth = ' + str(depth) + '\n'
        + 'Epsilon = ' + str(epsilon) + '\n'
        + 'Search = ' + str(search) + '\n'
        + 'Temperature = ' + str(temperature) + '\n')
    infoFile.close()
    print('Start MCTS epsilon and temperature sweep!')
    print('[Total games: %d]' % (nGames * len(epsilon) * len(temperature)))
    print(
        '[Depth: %d, Search: %d]'
        % (depth, search))
    HCAI = []
    for i in range(1):
        HCAI.append(c.actions[1])
    for i in range(35):
        HCAI.append(c.actions[0])
    bResultsFile = open('MCTS_sweepET_b.txt', 'w')
    wResultsFile = open('MCTS_sweepET_w.txt', 'w')
    
    # Run the parameter sweep
    for iEpsilon in range(len(epsilon)):
        for iTemperature in range(len(temperature)):
            print('Completed %1.1f' % (100 * (iEpsilon * len(epsilon) + iTemperature) / (len(epsilon) * len(temperature))) + '%')
            bMCTSAI = MonteCarloTreeSearchAI.AI(c.team2, c.team3, depth, epsilon[iEpsilon], search, temperature[iTemperature])
            bMCTSvHC = 0
            wMCTSAI = MonteCarloTreeSearchAI.AI(c.team3, c.team2, depth, epsilon[iEpsilon], search, temperature[iTemperature])
            wMCTSvHC = 0
            for iGame in range(nGames):
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
            bResultsFile.write(str(bMCTSvHC / nGames) + '\n')
            wResultsFile.write(str(wMCTSvHC / nGames) + '\n')
    print('Completed 100%')
    bResultsFile.close()
    wResultsFile.close()

if __name__ == '__main__':
    startTime = time.time()
    main()
    PrintTime.printTime(time.time() - startTime)

#