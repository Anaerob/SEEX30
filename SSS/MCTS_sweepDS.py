import numpy as np
import time

import Game
import Load
import MonteCarloTreeSearchAI
import PrintTime

def main():
    
    # Parameters
    nGames = 1000
    depth = [5, 10, 15, 20, 25]
    epsilon = 0.2
    search = [200, 400, 600, 800, 1000]
    temperature = 0.2
    
    # Initialize
    HCAI = []
    HC_string = ''
    game = Game.Game()
    for i in range(game.n - 1):
        HCAI.append(0)
        HC_string += '0'
    for i in range(game.n):
        HCAI.append(1)
        HC_string += '1'
    infoFile = open('MCTS_sweepDS_info.txt', 'w')
    infoFile.write(
        'Games = ' + str(nGames) + '\n'
        + 'Depth = ' + str(depth) + '\n'
        + 'Epsilon = ' + str(epsilon) + '\n'
        + 'Search = ' + str(search) + '\n'
        + 'Temperature = ' + str(temperature) + '\n')
    infoFile.close()
    print('Start MCTS depth and search sweep!')
    print('[Total games: %d]' % (nGames * len(depth) * len(search)))
    print(
        '[Epsilon: %1.1f, Temperature: %1.1f]'
        % (epsilon, temperature))
    resultsStrategyFile = open('MCTS_sweepDS_strategy.txt', 'w')
    resultsTimeFile = open('MCTS_sweepDS_time.txt', 'w')
    
    # Run the parameter sweep
    for iDepth in range(len(depth)):
        for iSearch in range(len(search)):
            print(
                'Completed %1.1f'
                % (100 * (iDepth * len(depth) + iSearch)
                    / (len(depth) * len(search)))
                + '%')
            strategies = {}
            runTime = time.time()
            for iGame in range(nGames):
                MCTSAI = MonteCarloTreeSearchAI.AI(
                    depth[iDepth],
                    epsilon,
                    search[iSearch],
                    temperature)
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
                resultsStrategyFile.write(str(strategies[HC_string] / nGames) + '\n')
            else:
                resultsStrategyFile.write(str(0.0) + '\n')
            resultsTimeFile.write(str((time.time() - runTime) / nGames) + '\n')
    print('Completed 100%')
    resultsStrategyFile.close()
    resultsTimeFile.close()

if __name__ == '__main__':
    startTime = time.time()
    main()
    PrintTime.printTime(time.time() - startTime)

#