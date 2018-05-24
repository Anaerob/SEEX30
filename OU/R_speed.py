import numpy as np
import time

import Constants as c
import Game
import FormatTime
import RandomAI

def main():
    
    # Parameters
    nGames = 1000
    limit = 100
    
    # Initialize
    AI = [RandomAI.AI(), RandomAI.AI()]
    
    # Run speed test
    runTimes = []
    for iGame in range(nGames):
        if iGame % int(nGames / 10) == 0:
            print('Completed ' + str(int(100 * iGame / nGames)) + '%')
        iTime = time.time()
        game = Game.Game(False)
        while game.running and game.round < limit:
            states = [game.getState(c.amBlack), game.getState(c.amWhite)]
            if game.forceSwitch[0] == game.forceSwitch[1]:
                game.trainers[0].setNextAction(AI[0].getAction(states[0]))
                game.trainers[1].setNextAction(AI[1].getAction(states[1]))
            else:
                for iT in range(2):
                    if game.forceSwitch[iT]:
                        game.trainers[iT].setNextAction(AI[iT].getAction(states[iT]))
            game.progress()
        runTimes.append(time.time() - iTime)
    sum = np.sum(runTimes)
    mean = sum / nGames
    standardDeviation = np.sqrt(np.sum((runTimes - mean) ** 2) / (nGames))
    print(
        'Completed 100%' + '\n'
        + 'Sum: ' + FormatTime.getString(sum) + '\n'
        + 'Mean: ' + FormatTime.getString(mean) + '\n'
        + 'Standard deviation: ' + FormatTime.getString(standardDeviation))

if __name__ == '__main__':
    main()

#