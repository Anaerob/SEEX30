import numpy as np
import time

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
    startTime = time.time()
    HCAI = []
    HC_string = ''
    game = Game.Game()
    for i in range(game.n - 1):
        HCAI.append(0)
        HC_string += '0'
    for i in range(game.n):
        HCAI.append(1)
        HC_string += '1'
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
    resultsFile = open('MCTS_sweepET.txt', 'w')
    
    # Run the parameter sweep
    for iEpsilon in range(len(epsilon)):
        for iTemperature in range(len(temperature)):
            print(
                'Completed %1.1f'
                % (100 * (iEpsilon * len(epsilon) + iTemperature)
                    / (len(epsilon) * len(temperature)))
                + '%')
            strategies = {}
            for iGame in range(nGames):
                MCTSAI = MonteCarloTreeSearchAI.AI(
                    depth,
                    epsilon[iEpsilon],
                    search,
                    temperature[iTemperature])
                game = Game.Game()
                MCTS_string = ''
                while game.running:
                    MCTS_action = MCTSAI.getAction(game.getState(True))
                    MCTS_string += str(MCTS_action)
                    game.progress([MCTS_action, HCAI[game.round]])
                if MCTS_string in strategies:
                    strategies[MCTS_string] += 1
                else:
                    strategies[MCTS_string] = 1
            if HC_string in strategies:
                resultsFile.write(str(strategies[HC_string] / nGames) + '\n')
            else:
                resultsFile.write(str(0.0) + '\n')
    print('Completed 100%')
    resultsFile.close()
    
    PrintTime.printTime(time.time() - startTime)

if __name__ == '__main__':
    main()

#