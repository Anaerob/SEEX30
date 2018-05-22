import numpy as np
import time

import Game
import Load
import MonteCarloTreeSearchAI
import PrintTime

def main():
    
    # Parameters
    nGames = 1000
    depth = 25
    epsilon = 0.2
    search = 1000
    temperature = 0.2
    
    # Initialize
    MCTSAI = MonteCarloTreeSearchAI.AI(depth, epsilon, search, temperature)
    HCAI = []
    HC_string = ''
    game = Game.Game()
    for i in range(game.n - 1):
        HCAI.append(0)
        HC_string += '0'
    for i in range(game.n):
        HCAI.append(1)
        HC_string += '1'
    print('Start MCTS benchmark!')
    print('[Total games: %d]' % (nGames))
    print(
        '[Depth: %d, Epsilon: %1.1f, Search: %d, Temperature: %1.1f]'
        % (depth, epsilon, search, temperature))
    strategies = {}
    MCTSvHC = 0
    
    # Run the benchmark
    for iGame in range(nGames):
        if iGame % int(nGames / 10) == 0:
            print('Completed ' + str(int(100 * iGame / nGames)) + '%')
        game = Game.Game()
        MCTS_string = ''
        while game.running:
            MCTS_action = MCTSAI.getAction(game.getState(True))
            MCTS_string += str(MCTS_action)
            game.progress([MCTS_action, HCAI[game.round]])
        if game.win[0]:
            MCTSvHC += 1
        if MCTS_string in strategies:
            strategies[MCTS_string] += 1
        else:
            strategies[MCTS_string] = 1
    print('Completed 100%')
    
    # Write the results
    resultsFile = open('MCTS_benchmark_results.txt', 'w')
    resultsFile.write('## Monte Carlo Tree Search\n')
    resultsFile.write(
        'Games: ' + str(nGames) + '\n'
        + 'Depth: ' + str(depth) + '\n'
        + 'Epsilon: ' + str(epsilon) + '\n'
        + 'Search: ' + str(search) + '\n'
        + 'Temperature: ' + str(temperature) + '\n\n')
    resultsFile.write('# Optimal strategy usage: \n')
    if HC_string in strategies:
        resultsFile.write(str(100 * strategies[HC_string] / nGames) + '%\n\n')
    else:
        resultsFile.write('Did not use the optimal strategy at all')
    resultsFile.write('# Win percentage: \n')
    resultsFile.write(str(100 * MCTSvHC / nGames) + '%\n\n')
    resultsFile.close()

if __name__ == '__main__':
    startTime = time.time()
    main()
    PrintTime.printTime(time.time() - startTime)

#