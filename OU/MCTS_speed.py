import math
import time

import Game
import FormatTime
import MonteCarloTreeSearchAI
import RandomAI

def main():
    
    # Parameters
    nGames = 10
    depth = 1
    epsilon = 0.1
    limit = 100
    search = 250
    temperature = 0.2
    
    # Initialize
    AI = [MonteCarloTreeSearchAI.AI(depth, epsilon, limit, search, temperature), RandomAI.AI()]
    
    # Run speed test
    runTimes = []
    for iGame in range(nGames):
        if iGame % int(nGames / 10) == 0:
            print('Completed ' + str(int(100 * iGame / nGames)) + '%')
        iTime = time.time()
        game = Game.Game()
        while game.running and game.round < limit:
            states = [game.getState(True), game.getState(False)]
            if game.forceSwitch[0] == game.forceSwitch[1]:
                game.nextAction[0] = AI[0].getAction(states[0])
                game.nextAction[1] = AI[1].getAction(states[1])
            else:
                for iT in range(2):
                    if game.forceSwitch[iT]:
                        game.nextAction[iT] = AI[iT].getAction(states[iT])
            game.progress()
        runTimes.append(time.time() - iTime)
    tSum = sum(runTimes)
    mean = tSum / nGames
    distance = []
    for i in range(nGames):
        distance.append((runTimes[i] - mean) ** 2)
    standardDeviation = math.sqrt(sum(distance) / nGames)
    print(
        'Completed 100%' + '\n'
        + 'Sum: ' + FormatTime.getString(tSum) + '\n'
        + 'Mean: ' + FormatTime.getString(mean) + '\n'
        + 'Standard deviation: ' + FormatTime.getString(standardDeviation))

if __name__ == '__main__':
    main()

#