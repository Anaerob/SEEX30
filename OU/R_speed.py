import math
import time

import FormatTime
import Game
import RandomAI
import Sim

def main():
    
    # Parameters
    nGames = 100000
    limit = 100
    
    # Initialize
    AI = [RandomAI.AI(), RandomAI.AI()]
    
    # Run speed test
    runTimes = []
    for iGame in range(nGames):
        if iGame % int(nGames / 10) == 0:
            print('Completed ' + str(int(100 * iGame / nGames)) + '%')
        iTime = time.time()
        game = Sim.Sim()
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